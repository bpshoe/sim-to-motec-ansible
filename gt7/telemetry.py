import struct
from enum import Enum
from collections import namedtuple
from datetime import datetime
from copy import copy
import logging
import asyncio
import json

from .database import Database

try:
    from Crypto.Cipher import Salsa20
except ImportError:
    try:
        from salsa20 import Salsa20_xor as Salsa20
    except ImportError:
        raise RuntimeError("Missing dependency 'salsa20' or 'pycryptodome'. Run 'pip install salsa20' or 'pip install pycryptodome'")



from gt7.writer.motec_exporter import export_to_ld
from .sampler import GT7Sampler

l = logging.getLogger(__name__)

Wheels = namedtuple("Wheels", ["fl", "fr", "rl", "rr"])

class Flags(Enum):
    IN_RACE = 0b0000000000000001
    PAUSED = 0b0000000000000010
    LOADING = 0b0000000000000100
    IN_GEAR = 0b0000000000001000
    HAS_TURBO = 0b0000000000010000
    REV_LIMIT = 0b0000000000100000
    HANDBRAKE = 0b0000000001000000
    LIGHTS = 0b0000000010000000
    LOWBEAM = 0b0000000100000000
    HIGHBEAM = 0b0000001000000000
    ASM = 0b0000010000000000
    TCS = 0b0000100000000000

class GT7Logger:
    channels = [
        'beacon', 'lap', 'rpm', 'gear', 
        'throttle', 'brake', 'clutch', 'steer', 
        'speed', 'lat', 'long',
        'velx', 'vely', 'velz', 'glat', 'gvert', 'glong', 
        'suspfl', 'suspfr', 'susprl', 'susprr',
        'wspdfl', 'wspdfr', 'wspdrl', 'wspdrr',
        'tyretempfl', 'tyretempfr', 'tyretemprl', 'tyretemprr',
        'rideheight',
        'turbopres',
        'oilpres', 'oiltemp', 'watertemp',
        { "name": "fuellevel", "units": "%" },
        'asm', 'tcs'
    ]

    def __init__(self,
                rawfile=None,
                sampler=None,
                filetemplate=None,
                replay=False,
                name="",
                session="",
                vehicle="",
                driver="",
                venue="", 
                comment="",
                shortcomment="",
                imperial=False,
                manager=None,
                db=None):
        
        self.sampler = sampler
        self.event = {
            "name": name,
            "session": session,
            "vehicle": vehicle,
            "driver": driver,
            "venue": venue,
            "comment": comment,
            "shortcomment": shortcomment
        }

        self.current_event = None
        self.last_packet = None
        self.skip_samples = 0
        self.track = None
        self.track_detector = None
        self.replay = replay
        self.queue = asyncio.Queue()
        self.manager = manager
        self.db = db

    


    async def _websocket_broadcaster_task(self):
        while True:
            try:
                timestamp, samples, is_lap = await self.queue.get()
                if not is_lap and self.manager:
                    data = dict(zip([c.get('name', c) for c in self.channels], samples))
                    data['timestamp'] = timestamp
                    await self.manager.broadcast(json.dumps(data))
                self.queue.task_done()
            except asyncio.CancelledError:
                l.info("WebSocket broadcaster task cancelled.")
                break
            except Exception as e:
                l.error(f"Error in WebSocket broadcaster task: {e}")

    async def _db_writer_task(self):
        while True:
            try:
                timestamp, samples, is_lap = await self.queue.get()
                if is_lap and self.db:
                    session_data = {
                        "driver": self.event.get("driver", ""),
                        "vehicle": self.event.get("vehicle", ""),
                        "venue": self.event.get("venue", ""),
                        "session": self.event.get("session", ""),
                        "best_lap": samples['laptime']
                    }
                    self.db.insert_session(session_data)
                self.queue.task_done()
            except asyncio.CancelledError:
                l.info("DB writer task cancelled.")
                break
            except Exception as e:
                l.error(f"Error in DB writer task: {e}")

    def get_latest_data(self):
        if self.last_packet:
            return {
                "RPM": self.last_packet.rpm,
                "Speed": self.last_packet.speed,
                "Gear": self.last_packet.gear,
                "Throttle": self.last_packet.throttle,
                "Brake": self.last_packet.brake,
                "Clutch": self.last_packet.clutch,
            }
        return None

    def process_sample(self, timestamp, sample):
        p = GT7DataPacket(sample)
        if not self.last_packet:
            self.last_packet = p
            l.info(f"received first packet from GT7 with ID {p.tick}")

        missing = range(self.last_packet.tick + 1, p.tick)
        if len(missing):
            l.info(f"misssed {len(missing)} ticks, duplicating {self.last_packet.tick}")
            for tick in missing:
                mp = copy(self.last_packet)
                mp.tick = tick
                self.process_packet(timestamp, mp)

        self.process_packet(timestamp, p)
        self.last_packet = p

    def process_packet(self, timestamp, packet):
        try:
            # This is a placeholder for the full decryption and parsing pipeline
            # For now, we'll create a dummy dataframe
            data = {
                'timestamp': [0, 0.01, 0.02],
                'throttle': [0, 10, 50],
                'brake': [100, 90, 20]
            }
            df = pd.DataFrame(data)

            metadata = {
                'vehicle': 'Placeholder Vehicle',
                'venue': 'Placeholder Track',
                'event': 'Placeholder Event'
            }

            output_path = self.config.get('log_output_path', './logs/session.ld')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            export_to_ld(df, metadata, output_path)
        except Exception:
            print("[DATAFRAME ERROR] Could not assemble dataframe.")
            sys.exit(1)

class GT7DataPacket:
    fmt = struct.Struct(
        "<"
        "4x"  # MAGIC
        "3f"  # POSITION
        "3f"  # VELOCITY
        "4f"  # ROTATION
        "12x" # VELOCITY_ANGULAR
        "f"   # RIDE_HEIGHT
        "f"   # RPM
        "4x"  # IV
        "f"   # CURRENT_FUEL
        "f"   # FUEL_CAPACITY
        "f"   # SPEED
        "f"   # TURBO_BOOST
        "f"   # OIL_PRESSURE
        "f"   # WATER_TEMP
        "f"   # OIL_TEMP
        "4f"  # TYRES_TEMP
        "i"   # TICK
        "2h"  # LAPS
        "i"   # BEST_LAPTIME
        "i"   # LAST_LAPTIME
        "4x"  # DAYTIME_PROGRESSION
        "2h"  # RACE_POSITION
        "h"   # REV_UPSHIFT
        "h"   # REV_LIMIT
        "2x"  # MAX_SPEED
        "H"   # FLAGS
        "B"   # GEAR
        "B"   # THROTTLE
        "B"   # BRAKE
        "x"   # UNKNOWN
        "16x" # ROAD_PLANE
        "4f"  # WHEELS_SPEED
        "4f"  # TYRES_RADIUS
        "4f"  # TYRE_SUSPENSION_TRAVEL
        "32x" # UNKNOWN_RESRVED
        "f"   # CLUCH
        "4x"  # CLUCH_ENGAGEMENT
        "4x"  # CLUCH_RPM
        "4x"  # TOP_SPEED
        "32x" # GEAR_RATIOS
        "I"   # CAR_CODE
    )

    size = fmt.size

    def __init__(self, buf, encrypted=True):
        try:
            if encrypted:
                buf = self.decrypt(buf)

            (
                px, py, pz,
                vx, vy, vz,
                rw, rx, ry, rz,
                self.ride_height,
                self.rpm,
                self.current_fuel,
                self.fuel_capacity,
                self.speed,
                self.turbo_boost,
                self.oil_pressure,
                self.water_temp,
                self.oil_temp,
                ttfl, ttfr, ttrl, ttrr,
                self.tick,
                self.current_lap,
                self.laps,
                self.best_laptime,
                self.last_laptime,
                self.race_position,
                self.rev_upshift,
                self.rev_limit,
                self.opponents,
                self.flags,
                gear,
                self.throttle,
                self.brake,
                wsfl, wsfr, wsrl, wsrr,
                wrfl, wrfr, wrrl, wrrr,
                susfl, susfr, susrl, susrr,
                self.clutch,
                self.car_code
            ) = self.fmt.unpack(buf)
        except Exception:
            print("[PARSING ERROR] Could not parse packet.")
            sys.exit(1)

        self.position = (px, py, pz)
        self.velocity = (vx, vy, vz)
        self.rotation = (rw, rx, ry, rz)

        self.tyretemp = Wheels(ttfl, ttfr, ttrl, ttrr)
        self.wheelspeed = Wheels(wsfl, wsfr, wsrl, wsrr)
        self.wheelradius = Wheels(wrfl, wrfr, wrrl, wrrr)
        self.suspension = Wheels(susfl, susfr, susrl, susrr)

        self.gear = gear & 0x0F
        self.suggested_gear = (gear & 0xF0) >> 4

        self.paused = bool(self.flags & Flags.PAUSED.value)
        self.in_race = bool(self.flags & Flags.IN_RACE.value)
        self.tcs_active = bool(self.flags & Flags.TCS.value)
        self.asm_active = bool(self.flags & Flags.ASM.value)

    @staticmethod
    def decrypt(dat):
        try:
            KEY = b'Simulator Interface Packet GT7 ver 0.0'
            oiv = dat[0x40:0x44]
            iv1 = int.from_bytes(oiv, byteorder='little')
            iv2 = iv1 ^ 0xDEADBEAF
            IV = bytearray()
            IV.extend(iv2.to_bytes(4, 'little'))
            IV.extend(iv1.to_bytes(4, 'little'))
            ddata = Salsa20.new(key=KEY[0:32], nonce=bytes(IV)).decrypt(dat)

            magic = int.from_bytes(ddata[0:4], byteorder='little')
            if magic != 0x47375330:
                return bytearray(b'')
            return ddata
        except Exception:
            print("[DECRYPTION ERROR] Invalid packet or wrong key. Check your config’s salsa20_key.")
            sys.exit(1)