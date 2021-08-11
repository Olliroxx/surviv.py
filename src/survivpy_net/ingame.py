from survivpy_net.custom_types import Vector
from logging import getLogger

constants = {
    "mapNameMaxLen": 0x18,
    "playerNameMaxLen": 0x10,
    "mouseMaxDist": 0x40,
    "smokeMaxRad": 0xa,
    "actionMaxDuration": 0xc,
    "airstrikeZoneMaxRad": 0x100,
    "airstrikeZoneMaxDuration": 0x3c,
    "playerMinScale": 0.75,
    "playerMaxScale": 0x2,
    "mapObjectMinScale": 0.125,
    "mapObjectMaxScale": 2.5,
    "maxPerks": 0x8,
    "maxMapIndicators": 0x10,
}
solved = []
log_xcodes = False
# Set to true to log de/encodings, except for
# type 6 as that might have a performance impact
logger = getLogger("survivpy_net")


def update_constants():
    global constants
    from json import load
    import pathlib
    constants_file = open(pathlib.Path(__file__).parent / "./configs/constants.json")
    constants = constants | load(constants_file)
    constants_file.close()

    mtypes_file = open(pathlib.Path(__file__).parent / "./configs/objects.json")
    mtypes_dict = load(mtypes_file)["objects"]
    mtypes_file.close()
    constants["mtypes"] = list(mtypes_dict.keys())
    constants["mtypes"].insert(0, "")

    files = ("bullets", "crosshairs", "heal_effects", "emotes", "explosions", "nonweapons", "guns", "melee_weapons",
             "outfits", "quests", "perks", "passes", "pings", "roles", "throwables", "default_unlocks", "xp_sources",
             "death_effects", "lootbox_tables", "item_pools", "xp_boost_events", "market_min_values", "npcs")
    gtypes_dict = {}
    for file in files:
        file = open(pathlib.Path(__file__).parent / ("./configs/" + file + ".json"))
        data = load(file)
        file.close()
        gtypes_dict = gtypes_dict | data
    constants["gtypes"] = list(gtypes_dict.keys())
    constants["gtypes"].insert(0, "")


class BitString:
    """
    Bitstring is a class that helps with the manipulation of binary data.

    It is based off the bitstring class in app.js, as that has slightly different behaviour to the python module ``bitstring``.

    Input buffer must be iterable yielding integers less than 256 (anything ``bytearray`` can use)

    Has multiple read/write functions for different data types with different sizes.

    Vector sizes are the sizes of the floats, not the total size.

    Full list:

       * read_ascii_str
       * read_bool
       * read_int8
       * read_uint8
       * read_int16
       * read_uint16
       * read_int32
       * read_uint32
       * read_float
       * read_float32
       * read_float64
       * read_bits (also needs bit amount)
       * read_vec
       * read_vec32
       * read_vec64

       * write_ascii_str
       * write_bool
       * write_int8
       * write_uint8
       * write_int16
       * write_uint16
       * write_int32
       * write_uint32
       * write_float32
       * write_float64
       * write_bits
       * write_vec
       * write_unit_vec

    """

    def __init__(self, buffer=None):
        """
        :param buffer: Input buffer, must be iterable yielding integers less than 256 (anything ``bytearray`` can use)
        """

        if buffer is None:
            buffer = bytes()

        if type(buffer) not in (bytearray, tuple, list, bytes):
            raise TypeError("Input buffer must be byteArray")
        else:
            buffer = bytearray(buffer)

        self._view = buffer

        self.index = 0

    def __len__(self):
        return len(self._view) * 8

    def __bytes__(self):
        return bytes(self._view)

    def __str__(self):
        return self.get_trimmed().hex()

    def _set_bit(self, offset, bit):
        if bit:
            self._view[offset >> 3] |= 1 << (offset & 7)
        else:
            self._view[offset >> 3] &= ~(1 << (offset & 7))

    def _get_bits(self, offset, length, signed=False):
        remaining = len(self._view) * 8 - offset
        if length > remaining:
            raise ValueError("Cannot get " + str(length) + " bit(s) from offset " + str(offset) + ", " + str(
                remaining) + " available")

        result = 0
        i = 0
        while i < length:
            left = length - i
            masked_offset = offset & 7
            byte = self._view[offset >> 3]
            size = min(left, 8 - masked_offset)
            unknown_2 = (1 << size) - 1
            bit = byte >> masked_offset & unknown_2

            result = result | bit << i
            offset = offset + size
            i = i + size

        if signed:
            highest_positive = 2 ** (length - 1)
            lowest_negative = -highest_positive
            if result >= highest_positive:
                return result - highest_positive + lowest_negative
        return result

    def _set_bits(self, offset, bits, length):
        free = len(self._view) * 8 - offset
        if length > free:
            raise ValueError(
                "Cannot set " + str(length) + " bit(s) from offset " + str(offset) + ", " + str(free) + " available")
        if bits > (2 ** length) - 1:
            raise ValueError("Value too large for amount of bits")

        buffer = 0
        while buffer < length:
            if length - buffer >= 8 and (offset & 7) == 0:
                self._view[offset >> 3] = bits & 255
                x = 8
            else:
                self._set_bit(offset, bits & 1)
                x = 1

            bits = bits >> x
            offset += x
            buffer = buffer + x

    def _get_bool(self, offset):
        return self._get_bits(offset, 1, False) != 0

    def _get_int8(self, offset):
        return self._get_bits(offset, 8, True)

    def _get_uint8(self, offset):
        return self._get_bits(offset, 8, False)

    def _get_int16(self, offset):
        return self._get_bits(offset, 16, True)

    def _get_uint16(self, offset):
        return self._get_bits(offset, 16, False)

    def _get_int32(self, offset):
        return self._get_bits(offset, 32, True)

    def _get_uint32(self, offset):
        return self._get_bits(offset, 32, False)

    def _get_float32(self, offset):
        bits = self._get_bits(offset, 32).to_bytes(4, "big")
        import struct
        return struct.unpack(">f", bits)[0]

    def _get_float64(self, offset):
        bits = self._get_bits(offset, 64).to_bytes(8, "big")
        import struct
        return struct.unpack(">d", bits)[0]

    def _set_bool(self, offset, boolean):
        self._set_bits(offset, int(boolean), 1)

    def _set_int8(self, offset, int8):
        self._set_bits(offset, int8, 8)

    def _set_uint8(self, offset, uint8):
        self._check_positive(uint8)
        self._set_bits(offset, uint8, 8)

    def _set_int16(self, offset, int16):
        self._set_bits(offset, int16, 16)

    def _set_uint16(self, offset, uint16):
        self._check_positive(uint16)
        self._set_bits(offset, uint16, 16)

    def _set_int32(self, offset, int32):
        self._set_bits(offset, int32, 32)

    def _set_uint32(self, offset, uint32):
        self._check_positive(uint32)
        self._set_bits(offset, uint32, 32)

    def _set_float32(self, offset, float32):
        import struct
        packed = struct.pack(">f", float32)
        self._set_bits(offset, int.from_bytes(packed, "big"), 32)

    def _get_array_buffer(self, offset, elements):
        result = list(elements)

        i = 0
        while i < elements:
            result[i] = self._get_uint8(offset + i * 8)
            i += 1

    def read_ascii_str(self, length=None):
        """
        Read an ASCII string.

        At time of writing, surviv uses no unicode

        .. warning::
            There is currently no unicode support

        :param length: If left unfilled, will read until a null byte, else will read a string this long
        :return: result string
        """
        result = self._read_str(self, length, False)
        return result

    def read_utf8_str(self, length=None):
        return self._read_str(self, length, True)

    @staticmethod
    def _read_str(bitstring, length, z: bool):
        if length == 0:
            return ""

        byte_no = 0
        output_list = []
        not_last_byte = True
        unk_var_4 = bool(length)
        if not length:
            length = (len(bitstring) - bitstring.index) // 8
        else:
            length += 1  # Minor difference in implementation mean this is necessary

        while byte_no < length:
            byte = bitstring.read_uint8()
            if byte == 0:
                not_last_byte = False
                if not unk_var_4:
                    break
            if not_last_byte:
                output_list.append(byte)
            byte_no += 1

        str_trim = ""
        for charcode in output_list:
            str_trim = str_trim + chr(charcode)
        if z:
            from urllib.parse import unquote, quote
            return unquote(quote(str_trim))
            # Unicode magic I think?
            # Original JS:
            # return decodeURIComponent(escape(_0xb6109a));
        else:
            return str_trim

    @staticmethod
    def _write_ascii_string(bitstring, string, length):

        for num in range(length if length is not None else len(string)):
            if num + 1 > len(string):
                char = "\x00"
            else:
                char = string[num]
            bitstring.write_uint8(ord(char))
        if length is None:
            bitstring.write_uint8(0)

    def _write_utf8_string(self, bitstring, string):
        array = self._string_to_list(string)

        for element in array:
            bitstring.write_uint8(element)

    @staticmethod
    def _string_to_list(string):
        array = []

        i = 0
        while i < len(string):
            charcode = ord(string[i])
            if charcode < 128:
                array.append(charcode)
            elif charcode < 2048:
                array.append(charcode >> 6 | 192)
                array.append(charcode & 63 | 128)
            elif charcode < 65534:
                array.append(charcode >> 12 | 224)
                array.append(charcode >> 6 & 63 | 128)
                array.append(charcode & 63 | 128)
            else:
                array.append(charcode >> 18 | 240)
                array.append(charcode >> 12 & 63 | 128)
                array.append(charcode >> 6 & 63 | 128)
                array.append(charcode & 63 | 128)
            i += 1
        return array

    def read_bool(self):
        result = self._get_bool(self.index)
        self.index += 1
        return result

    def read_int8(self):
        result = self._get_int8(self.index)
        self.index += 8
        return result

    def read_uint8(self):
        result = self._get_uint8(self.index)
        self.index += 8
        return result

    def read_int16(self):
        result = self._get_int16(self.index)
        self.index += 16
        return result

    def read_uint16(self):
        result = self._get_uint16(self.index)
        self.index += 16
        return result

    def read_int32(self):
        result = self._get_int32(self.index)
        self.index += 32
        return result

    def read_uint32(self):
        result = self._get_uint32(self.index)
        self.index += 32
        return result

    def read_float(self, minimum, maximum, size):
        max_val = 2 ** size - 1
        numerator = self.read_bits(size)
        fraction = numerator / max_val
        return minimum + fraction * (maximum - minimum)

    def read_float32(self):
        result = self._get_float32(self.index)
        self.index += 32
        return result

    def read_float64(self):
        result = self._get_float64(self.index)
        self.index += 64
        return result

    def read_bits(self, amount):
        result = self._get_bits(self.index, amount)
        self.index += amount
        return result

    def read_vec(self, xMin, yMin, xMax, yMax, size):
        x = self.read_float(xMin, xMax, size)
        y = self.read_float(yMin, yMax, size)
        return x, y

    def read_unit_vec(self, size):
        return self.read_vec(-1.0001, -1.0001, 1.0001, 1.0001, size)

    def read_vec16(self):
        return self.read_vec(0, 0, 1024, 1024, 16)

    def read_vec32(self):
        x = self.read_float32()
        y = self.read_float32()
        result = (x, y)
        return result

    def read_vec64(self):
        x = self.read_float64()
        y = self.read_float64()
        result = (x, y)
        return result

    def write_bool(self, boolean):
        self._set_bool(self.index, boolean)
        self.index += 1

    def write_int8(self, int8):
        self._set_int8(self.index, int8)
        self.index += 8

    def write_uint8(self, uint8):
        self._set_uint8(self.index, uint8)
        self.index += 8

    def write_int16(self, int16):
        self._set_int16(self.index, int16)
        self.index += 16

    def write_uint16(self, uint16):
        self._set_uint16(self.index, uint16)
        self.index += 16

    def write_int32(self, int32):
        self._set_int32(self.index, int32)
        self.index += 32

    def write_uint32(self, uint32):
        self._set_uint32(self.index, uint32)
        self.index += 32

    def write_float32(self, float32):
        self._set_float32(self.index, float32)
        self.index += 32

    def write_bits(self, bits, length):
        self._set_bits(self.index, bits, length)
        self.index += length

    def write_ascii_str(self, text: str, length=None):
        self._write_ascii_string(self, text, length)

    def write_float(self, val, mini, maxi, size):
        from math import floor
        step_count = (1 << size) - 1
        clamped = sorted([val, mini, maxi])[1]
        fraction = (clamped - mini) / (maxi - mini)
        result = fraction * step_count + 0.5

        self.write_bits(floor(result), size)

    def write_vec(self, xMin, yMin, xMax, yMax, x, y, size):
        self.write_float(x, xMin, xMax, size)
        self.write_float(y, yMin, yMax, size)

    def write_unit_vec(self, val, size):
        self.write_vec(-1.0001, -1.0001, 1.0001, 1.0001, val[0], val[1], size)

    def write_utf8_str(self, text: str):
        self._write_utf8_string(self, text)

    def bits_free(self):
        return len(self) - self.index

    def write_align_to_next_byte(self):
        self._view = self._view.rstrip(b"\x00") + b"\x00"

    def read_align_to_next_byte(self):
        bits_to_read = 8 - (self.index % 8)
        if bits_to_read != 8:
            self.read_bits(bits_to_read)

    def get_view(self):
        return self._view

    @staticmethod
    def _check_positive(num):
        if num < 0:
            raise ValueError("Number is not positive")

    def get_trimmed(self):
        from math import ceil
        end = ceil(self.index/8)
        return bytes(self)[:end]


class TypedBitString(BitString):
    """
    This class is a bitstring that can also read and write (game) object types
    """

    def __init__(self, buffer=None):
        super().__init__(buffer)

        self.map_type_size = 12

        self.game_type_size = 10

    @staticmethod
    def _type_to_id(type_: str, types):
        return types.index(type_)

    @staticmethod
    def _id_to_type(num: int, types):
        return types[num]

    def read_game_type(self):
        num = self.read_bits(self.game_type_size)
        return self._id_to_type(num, constants["gtypes"])

    def write_game_type(self, gtype):
        num = self._type_to_id(gtype, constants["gtypes"])
        self.write_bits(num, self.game_type_size)

    def read_map_type(self):
        num = self.read_bits(self.map_type_size)
        return self._id_to_type(num, constants["mtypes"])

    def write_map_type(self, mtype):
        num = self._type_to_id(mtype, constants["mtypes"])
        self.write_bits(num, self.map_type_size)


class Packet:
    """
    Packet is a template class for the decoders/encoders used in a game session
    """

    def __init__(self, encode_data=None, bytearray_data=None):

        if bytearray_data is not None:
            if type(bytearray_data) in (bytes, bytearray, BitString, TypedBitString):
                self.data = TypedBitString(bytearray_data)
            elif type(bytearray_data) == str:
                self.data = TypedBitString(bytearray.fromhex(bytearray_data))
            else:
                raise ValueError("Invalid data type " + str(type(bytearray_data)))
        elif encode_data is not None:
            self.encode(encode_data)
        else:
            raise ValueError("Must have at least one of bytearray_data or encode_data")

    def __len__(self):
        return len(self.data)

    def __bytes__(self):
        return bytes(self.data)

    def encode(self, data):
        raise NotImplementedError("This should be overridden")

    def decode(self, game_state):
        raise NotImplementedError("This should be overridden")

    def get_trimmed(self):
        return self.data.get_trimmed()


class Type01Packet(Packet):

    def encode(self, fields):
        self.data = TypedBitString(bytearray(17 * 1024))
        self.data.write_uint8(1)
        self.data.write_uint32(fields["protocol"])
        self.data.write_ascii_str(fields["matchPriv"])
        self.data.write_ascii_str(fields["loadoutPriv"])
        self.data.write_ascii_str(fields["loadoutStats"])
        self.data.write_bool(fields["hasGoldenBP"])
        self.data.write_ascii_str(fields["questPriv"])
        self.data.write_ascii_str(fields["name"], constants["playerNameMaxLen"])
        self.data.write_bool(fields["isUnlinked"])
        self.data.write_bool(fields["useTouch"])
        self.data.write_bool(fields["isMobile"])
        self.data.write_bool(fields["proxy"])
        self.data.write_bool(fields["otherProxy"])
        self.data.write_bool(fields["bot"])
        self.data.write_bool(fields["autoMelee"])
        self.data.write_bool(fields["aimAssist"])
        self.data.write_ascii_str(fields["kpg"])
        self.data.write_align_to_next_byte()
        if log_xcodes:
            logger.debug("Encoded type 1")
            logger.debug("In: " + str(fields))
            logger.debug("Out: " + str(self.data))

    def decode(self, game_state):
        raise NotImplementedError("Type 1 packets should not be decoded client side")


class Type02Packet(Packet):

    def encode(self, data):
        raise NotImplementedError("Type 2 packets should not be encoded client side")

    def decode(self, game_state):
        self.data.read_uint8()
        result = {
            "reason": self.data.read_ascii_str()
        }
        game_state.status = "closed"
        if log_xcodes:
            logger.debug("Decoded type 2")
            logger.debug("In: " + str(self.data))
            logger.debug("Out: " + str(result))
        return result


class Type03Packet(Packet):
    def encode(self, data):
        self.data = TypedBitString(bytearray(128))
        self.data.write_uint8(data["seq"])
        for item in (
                "moveLeft", "moveRight", "moveUp", "moveDown", "shootStart", "shootHold", "portrait",
                "touchMoveActive"):
            self.data.write_bool(data[item])
        if data["touchMoveActive"]:
            self.data.write_unit_vec(Vector(data["touchMoveDir"]), 8)
            self.data.write_uint8(data["touchMoveLen"])
        self.data.write_unit_vec(Vector(data["toMouseDir"]), 10)
        self.data.write_float(data["toMouseLen"], 0, constants["mouseMaxDist"], 8)
        self.data.write_bits(len(data["inputs"]), 4)
        for item in data["inputs"]:
            self.data.write_uint8(item)
        self.data.write_game_type(data["useItem"])
        self.data.write_bits(0, 6)
        if log_xcodes:
            logger.debug("Encoded type 3")
            logger.debug("In: " + str(data))
            logger.debug("Out: " + str(self.data))

    def decode(self, game_state):
        raise NotImplementedError("Type 3 packets should not be decoded client side")


class Type05Packet(Packet):
    def encode(self, data):
        raise NotImplementedError("Type 5 packets should not be encoded client side")

    def decode(self, game_state):
        self.data.read_uint8()
        game_state.status = "joined"
        result = {
            "teamMode": self.data.read_uint8(),
            "playerId": self.data.read_uint16(),
            "started": self.data.read_bool(),
            "emoteCount": self.data.read_uint8(),
        }
        emotes = []
        for _ in range(result["emoteCount"]):
            emote = self.data.read_game_type()
            emotes.append(emote)
        result["emotes"] = emotes

        game_state.team_size = result["teamMode"]
        game_state.player_id = result["playerId"]
        self.data.read_align_to_next_byte()
        if log_xcodes:
            logger.debug("Decoded type 5")
            logger.debug("In: " + str(self.data))
            logger.debug("Out: " + str(result))
        return result


# noinspection PyUnusedLocal
class Type06Packet(Packet):

    def encode(self, data):
        raise NotImplementedError("Type 6 packets should not be encoded client side")

    def decode(self, game_state):
        self.data.read_uint8()
        operations = self._get_operations(self.data)

        del_obj_ids = []
        if "has_del_objs" in operations:
            del_obj_count = self.data.read_uint16()
            for _ in range(del_obj_count):
                del_obj_ids.append(self.data.read_uint16())

        full_objs = []
        if "has_full_objs" in operations:
            full_obj_count = self.data.read_uint16()
            for _ in range(full_obj_count):
                obj = {
                    "type": self.data.read_uint8(),
                    "id": self.data.read_uint16()
                }
                part_decoded = self.decode_obj_part(obj)
                full_decoded = self.decode_obj_full(obj)
                obj = obj | full_decoded | part_decoded
                full_objs.append(obj)

        part_obj_count = self.data.read_uint16()
        part_objs = []
        for _ in range(part_obj_count):
            part_obj = {"id": self.data.read_uint16()}
            if part_obj["id"] == game_state.player_id or part_obj["id"] == 3551:
                try:
                    obj = game_state.map.objects[part_obj["id"]]
                except KeyError:
                    obj = {
                        "type": 1
                    }
                # The current player uses the playerId as their object id, so theres nothing in map.objects
            else:
                obj = game_state.map.objects[part_obj["id"]]

            part_obj["type"] = obj["type"]
            part_obj = part_obj | self.decode_obj_part(part_obj)
            part_objs.append(obj | part_obj)

        if "has_active_player" in operations:
            game_state.active_player_id = self.data.read_uint16()
        game_state.activePlayer = self._decode_active_player(self.data)

        if "has_gas" in operations:
            game_state.map.gas = {
                "mode": self.data.read_uint8(),
                "duration": self.data.read_bits(8),
                "posOld": self.data.read_vec16(),
                "posNew": self.data.read_vec16(),
                "radOld": self.data.read_float(0, 2048, 16),
                "radNew": self.data.read_float(0, 2048, 16)
            }

        if "has_gas_circle" in operations:
            game_state.map.gasT = self.data.read_float(0, 1, 16)

        player_infos = []
        if "has_player_infos" in operations:
            player_info_count = self.data.read_uint8()
            for _ in range(player_info_count):
                player = self._decode_player_info(self.data)
                if player["id"] in game_state.player_infos:
                    player_infos.append(game_state.playerInfos[player["id"]] | player)
                else:
                    player_infos.append(player)

        del_player_ids = []
        if "has_del_player_ids" in operations:
            del_player_count = self.data.read_uint8()
            for _ in range(del_player_count):
                del_player_ids.append(self.data.read_uint16())

        if "has_player_status" in operations:
            status_count = self.data.read_uint8()
            game_state.playerStatuses = []
            for _ in range(status_count):
                if self.data.read_bool():
                    player = {
                        "pos": self.data.read_vec(0, 0, 1024, 1024, 11),
                        "visible": self.data.read_bool(),
                        "dead": self.data.read_bool(),
                        "downed": self.data.read_bool(),
                        "hasRole": self.data.read_bool()
                    }
                    if player["hasRole"]:
                        player["role"] = self.data.read_game_type()
                    game_state.playerStatuses.append(player)
            self.data.read_align_to_next_byte()

        if "has_group_status" in operations:
            game_state.groupStatus = []
            player_count = self.data.read_uint8()
            for _ in range(player_count):
                player = {
                    "health": self.data.read_float(0, 100, 7),
                    "disconnected": self.data.read_bool()
                }
                game_state.groupStatus.append(player)

        if "has_bullets" in operations:
            bullet_count = self.data.read_uint8()
            for _ in range(bullet_count):
                game_state.map.bullets.append(self._decode_bullet(self.data))

        if "has_explosions" in operations:
            explosion_count = self.data.read_uint8()
            for _ in range(explosion_count):
                explosion = {
                    "pos": self.data.read_vec16(),
                    "type": self.data.read_game_type(),
                    "layer": self.data.read_bits(2),
                }
                game_state.map.explosions.append(explosion)

        if "has_emotes" in operations:
            emote_count = self.data.read_uint8()
            for _ in range(emote_count):
                emote = {
                    "playerId": self.data.read_uint16(),
                    "type": self.data.read_game_type(),
                    "itemType": self.data.read_game_type(),
                    "isPing": self.data.read_bool()
                }
                if emote["isPing"]:
                    emote["pos"] = self.data.read_vec16()
                self.data.read_bits(3)
                game_state.map.emotes.append(emote)

        if "has_planes" in operations:
            plane_count = self.data.read_uint8()
            for _ in range(plane_count):
                plane = {"id": self.data.read_uint8()}
                incorrect_pos = self.data.read_vec(0, 0, 2048, 2038, 10)
                plane["pos"] = (incorrect_pos[0] - 512, incorrect_pos[1] - 512)
                plane["dir"] = self.data.read_unit_vec(8)
                plane["actionComplete"] = self.data.read_bool()
                plane["action"] = self.data.read_bits(3)
                game_state.map.planes.append(plane)

        if "has_airstrike_zones" in operations:
            zone_count = self.data.read_uint8()
            for _ in range(zone_count):
                game_state.map.airstrike_zones.append({
                    "pos": self.data.read_vec(0, 0, 1024, 1024, 12),
                    "rad": self.data.read_float(0, constants["airstrikeZoneMaxRad"], 8),
                    "duration": self.data.read_float(0, constants["airstrikeZoneMaxDuration"], 8),
                })

        if "has_map_indicators" in operations:
            indicator_count = self.data.read_uint8()
            for _ in range(indicator_count):
                game_state.map.map_indicators.append({
                    "id": self.data.read_bits(4),
                    "dead": self.data.read_bool(),
                    "equipped": self.data.read_bool(),
                    "type": self.data.read_game_type(),
                    "pos": self.data.read_vec16()
                })

        if "has_kill_leader" in operations:
            game_state.killLeader = {
                "id": self.data.read_uint16(),
                "kills": self.data.read_uint8()
            }

        self.data.read_align_to_next_byte()

        for item in part_objs:
            game_state.map.objects[item["id"]] = game_state.map.objects[item["id"]] | item

        for item in full_objs:
            game_state.map.objects[item["id"]] = item

        for item in player_infos:
            if item["id"] in game_state.player_infos:
                item = game_state.player_infos[item["id"]] | item
            game_state.player_infos[item["id"]] = item

        global solved
        for item in operations:
            if item not in solved:
                solved.append(item)

    @staticmethod
    def _get_operations(bs: TypedBitString):
        op_types = (
            "has_del_objs", "has_full_objs", "has_active_player", "has_gas", "has_gas_circle", "has_player_infos",
            "has_del_player_ids", "has_player_status", "has_group_status", "has_bullets", "has_explosions",
            "has_emotes",
            "has_planes", "has_airstrike_zones", "has_map_indicators", "has_kill_leader")
        operations = bs.read_uint16()
        out = []
        for item in range(len(op_types)):
            if bool(operations & 1 << item):
                out.append(op_types[item])
        return out

    @staticmethod
    def _decode_bullet(bs: TypedBitString):
        bullet = {
            "sourcePlayerId": bs.read_uint16(),
            "pos": bs.read_vec16(),
            "dir": bs.read_unit_vec(8),
            "bulletType": bs.read_game_type(),
            "layer": bs.read_bits(2),
            "varianceT": bs.read_float(0, 1, 4),
            "distAdjIdx": bs.read_bits(4),
            "clipDistance": bs.read_bool()
        }
        if bullet["clipDistance"]:
            bullet["distance"] = bs.read_float(0, 1024, 16)
        bullet["shotFx"] = bs.read_bool()
        if bullet["shotFx"]:
            bullet = bullet | {
                "shotSourceType": bs.read_game_type(),
                "shotOffhand": bs.read_bool(),
                "lastShot": bs.read_bool()
            }
        bullet["reflectCount"] = 0
        bullet["reflectObjId"] = 0
        bullet["hasReflected"] = bs.read_bool()
        if bullet["hasReflected"]:
            bullet["reflectCount"] = bs.read_bits(2)
            bullet["reflectObjId"] = bs.read_uint16()
        bullet["hasSpecialFx"] = bs.read_bool()
        if bullet["hasSpecialFx"]:
            bullet["shotAlt"] = bs.read_bool()
            bullet["splinter"] = bs.read_bool()
            bullet["trailSaturated"] = bs.read_bool()
            bullet["trailSmall"] = bs.read_bool()
            bullet["trailThick"] = bs.read_bool()
        return bullet

    @staticmethod
    def _decode_player_info(bs: TypedBitString):
        player = {
            "id": bs.read_uint16(),
            "teamId": bs.read_uint8(),
            "groupId": bs.read_uint8(),
            "name": bs.read_ascii_str(),
            "loadout": {
                "outfit": bs.read_game_type(),
                "heal": bs.read_game_type(),
                "boost": bs.read_game_type(),
                "melee": bs.read_game_type(),
                "deathEffect": bs.read_game_type(),
                "emotes": []
            }
        }
        for _ in range(constants["EmoteSlot"]["Count"]):
            player["loadout"]["emotes"].append(bs.read_game_type())

        player["userId"] = bs.read_uint32()
        player["isUnlinked"] = bs.read_bool()
        bs.read_align_to_next_byte()

        return player

    @staticmethod
    def _decode_active_player(bs: TypedBitString):
        output = {}
        if bs.read_bool():
            output["health"] = bs.read_float(0, 100, 8)
        if bs.read_bool():
            output["boost"] = bs.read_float(0, 100, 8)

        special_mode_effects = bs.read_bits(3)

        if special_mode_effects == 1:
            if bs.read_bool():
                output["luck"] = bs.read_float(0, 100, 8)
            # St patricks

        elif special_mode_effects == 2:
            if bs.read_bool():
                output["wetPercentage"] = bs.read_float(0, 100, 8)
            # Summer

        elif special_mode_effects == 3:
            if bs.read_bool():
                output["contactPercentage"] = bs.read_float(0, 100, 8)
            # Contact

        elif special_mode_effects == 4:
            if bs.read_bool():
                output["burningPercentage"] = bs.read_float(0, 100, 8)
            if bs.read_bool():
                output["nitroLacePercentage"] = bs.read_float(0, 100, 8)
            # Inferno

        if bs.read_bool():
            output["zoom"] = bs.read_uint8()

        if bs.read_bool():
            output["action"] = {
                "time": bs.read_float(0, constants["actionMaxDuration"], 8),
                "duration": bs.read_float(0, constants["actionMaxDuration"], 8),
                "targetId": bs.read_uint16()
            }

        if bs.read_bool():
            output["inventory"] = {"scope": bs.read_game_type()}
            for item in constants["bagSizes"]:
                output["inventory"][item] = 0
                if bs.read_bool():
                    output["inventory"][item] = bs.read_bits(9)

        if bs.read_bool():
            output["curWeaponIdx"] = bs.read_bits(2)
            output["weapons"] = []
            for _ in range(constants["WeaponSlot"]["Count"]):
                output["weapons"].append({
                    "type": bs.read_game_type(),
                    "ammo": bs.read_uint8(),
                })

        if bs.read_bool():
            output["spectatorCount"] = bs.read_uint8()

        bs.read_align_to_next_byte()
        return output

    @staticmethod
    def _obj_none_part(bs: TypedBitString):
        return {}

    @staticmethod
    def _obj_none_full(bs: TypedBitString):
        return {}

    @staticmethod
    def _obj_player_part(bs: TypedBitString):
        return {
            "pos": bs.read_vec16(),
            "dir": bs.read_unit_vec(8)
        }

    @staticmethod
    def _obj_player_full(bs: TypedBitString):
        output = {
            "outfit": bs.read_game_type(),
            "backpack": bs.read_game_type(),
            "helmet": bs.read_game_type(),
            "chest": bs.read_game_type(),
            "curWeapType": bs.read_game_type(),
            "layer": bs.read_bits(2),
            "dead": bs.read_bool(),
            "downed": bs.read_bool(),
            "animType": bs.read_bits(3),
            "animSeq": bs.read_bits(3),
            "actionType": bs.read_bits(3),
            "actionSeq": bs.read_bits(3),
            "wearingPan": bs.read_bool(),
            "playerIndoors": bs.read_bool(),
            "gunLoaded": bs.read_bool(),
            "passiveHeal": bs.read_bool(),
            "healByItemEffect": bs.read_bool(),
            "hasHaste": bs.read_bool()
        }

        if output["hasHaste"]:
            output["hasteType"] = bs.read_bits(3)
            output["hasteSeq"] = bs.read_bits(3)
        else:
            output["hasteType"] = 0
            output["hasteSeq"] = -1

        output["hasActionItem"] = bs.read_bool()
        if output["hasActionItem"]:
            output["actionItem"] = bs.read_game_type()
        else:
            output["actionItem"] = ""

        output["isScaled"] = bs.read_bool()
        if output["isScaled"]:
            output["playerScale"] = bs.read_float(constants['PlayerMinScale'], constants['PlayerMaxScale'], 8)
        else:
            output["playerScale"] = 1

        output["hasRole"] = bs.read_bool()
        if output["hasRole"]:
            output["role"] = bs.read_game_type()
        else:
            output["role"] = ""

        output["perks"] = []
        output["hasPerks"] = bs.read_bool()
        if output["hasPerks"]:
            output["perkCount"] = bs.read_bits(3)
            for _ in range(output["perkCount"]):
                output["perks"].append({
                    "type": bs.read_game_type(),
                    "droppable": bs.read_bool()
                })

        output["specialModeEffects"] = bs.read_bits(4)

        if output["specialModeEffects"] == 1:
            output["wearingLasrSwrd"] = bs.read_bool()
            output["pulseBoxEffect"] = bs.read_bool()
            output["movedByPulseBoxEffect"] = bs.read_bool()
            # May 4th

        elif output["specialModeEffects"] == 2:
            output["isTarget"] = bs.read_bool()
            output["infectedEffect"] = bs.read_bool()
            output["playerTransparent"] = bs.read_bool()
            output["biteEffect"] = bs.read_bool()
            # Contact

        elif output["specialModeEffects"] == 3:
            output["frozen"] = bs.read_bool()
            output["frozenOri"] = bs.read_bits(2)
            output["freezeLevel"] = bs.read_float(0, 5, 8)
            output["freezeActive"] = bs.read_bool()
            output["flaskEffect"] = bs.read_bool()
            # Snow

        elif output["specialModeEffects"] == 4:
            output["frenemy"] = bs.read_bool()
            output["chocolateBoxEffect"] = bs.read_bool()
            # Valentines

        elif output["specialModeEffects"] == 5:
            output["luckyEffect"] = bs.read_bool()
            output["savedByLuckEffect"] = bs.read_bool()
            output["loadingBlaster"] = bs.read_float(0, 1, 7)
            # St patricks

        elif output["specialModeEffects"] == 6:
            output["wetEffect"] = bs.read_bool()
            output["watermelonEffect"] = bs.read_bool()
            # Beach

        elif output["specialModeEffects"] == 7:
            output["gunchildaEffect"] = bs.read_bool()
            # Cinco de mayo

        elif output["specialModeEffects"] == 8:
            output["sugarRush"] = bs.read_bool()
            output["playSoundSugarRush"] = bs.read_bool()
            # Easter

        elif output["specialModeEffects"] == 9:
            output["windDir"] = bs.read_bits(2)
            output["hailDamageEffect"] = bs.read_bool()
            # Storm

        elif output["specialModeEffects"] == 10:
            output["burningEffect"] = bs.read_bool()
            output["nitroLaceEffect"] = bs.read_bool()
            # Inferno

        if constants["features"]["inGameNotificationActive"]:
            output["questCount"] = bs.read_bits(2)
            output["quests"] = []
            for _ in range(output["questCount"]):
                quest = {
                    "type": bs.read_bits(5),
                    "progress": bs.read_bits(11)
                }
                output["quests"].append(quest)

        bs.read_align_to_next_byte()
        return output

    @staticmethod
    def _obj_obstacle_part(bs: TypedBitString):
        result = {
            "pos": bs.read_vec16(),
            "ori": bs.read_bits(2),
            "scale": bs.read_float(constants["mapObjectMinScale"], constants["mapObjectMaxScale"], 8)
        }
        bs.read_bits(6)
        return result

    @staticmethod
    def _obj_obstacle_full(bs: TypedBitString):
        output = {
            "healthT": bs.read_float(0, 1, 8),
            "obj_type": bs.read_map_type(),
            "obstacleType": bs.read_ascii_str(),
            "layer": bs.read_bits(2),
            "dead": bs.read_bool(),
            "isDoor": bs.read_bool(),
            "teamId": bs.read_uint8()
        }

        if output["isDoor"]:
            output["door"] = {
                "open": bs.read_bool(),
                "canUse": bs.read_bool(),
                "locked": bs.read_bool(),
                "seq": bs.read_bits(5)
            }

        output["isButton"] = bs.read_bool()
        if output["isButton"]:
            output["button"] = {
                "onOff": bs.read_bool(),
                "canUse": bs.read_bool(),
                "seq": bs.read_bits(6)
            }

        output["isPuzzlePiece"] = bs.read_bool()
        if output["isPuzzlePiece"]:
            output["parentBuildingId"] = bs.read_uint16()

        output["isSkin"] = bs.read_bool()
        if output["isSkin"]:
            output["skinPlayerId"] = bs.read_uint16()

        bs.read_bits(5)
        return output

    @staticmethod
    def _obj_loot_part(bs: TypedBitString):
        return {
            "pos": bs.read_vec16()
        }

    @staticmethod
    def _obj_loot_full(bs: TypedBitString):
        output = {
            "obj_type": bs.read_game_type(),
            "count": bs.read_uint8(),
            "layer": bs.read_bits(2),
            "isOld": bs.read_bool(),
            "isPreloadedGun": bs.read_bool(),
            "hasOwner": bs.read_bool()
        }
        if output["hasOwner"]:
            output["ownerId"] = bs.read_uint16()

        bs.read_bits(1)
        return output

    @staticmethod
    def _obj_loot_spawner_part(bs: TypedBitString):
        output = {
            "pos": bs.read_vec16(),
            "obj_type": bs.read_map_type(),
            "layer": bs.read_bits(2)
        }
        bs.read_bits(2)
        return output

    @staticmethod
    def _obj_loot_spawner_full(bs: TypedBitString):
        return {}

    @staticmethod
    def _obj_dead_body_part(bs: TypedBitString):
        return {
            "pos": bs.read_vec16()
        }

    @staticmethod
    def _obj_dead_body_full(bs: TypedBitString):
        return {
            "layer": bs.read_uint8(),
            "playerId": bs.read_uint16()
        }

    @staticmethod
    def _obj_building_part(bs: TypedBitString):
        output = {
            "ceilingDead": bs.read_bool(),
            "occupied": bs.read_bool(),
            "ceilingDamaged": bs.read_bool(),
            "hasPuzzle": bs.read_bool()
        }
        if output["hasPuzzle"]:
            output["puzzleSolved"] = bs.read_bool()
            output["puzzleErrSeq"] = bs.read_bits(7)

        bs.read_bits(4)
        return output

    @staticmethod
    def _obj_building_full(bs: TypedBitString):
        return {
            "pos": bs.read_vec16(),
            "obj_type": bs.read_map_type(),
            "ori": bs.read_bits(2),
            "layer": bs.read_bits(2)
        }

    @staticmethod
    def _obj_structure_part(bs: TypedBitString):
        return {}

    @staticmethod
    def _obj_structure_full(bs: TypedBitString):
        output = {
            "pos": bs.read_vec16(),
            "obj_type": bs.read_map_type(),
            "ori": bs.read_bits(2),
            "interiorSoundEnable": bs.read_bool(),
            "interiorSoundAlt": bs.read_bool(),
            "layerObjIds": []
        }

        for _ in range(constants["structureLayerCount"]):
            output["layerObjIds"].append(bs.read_uint16())
        return output

    @staticmethod
    def _obj_decal_part(bs: TypedBitString):
        return {}

    @staticmethod
    def _obj_decal_full(bs: TypedBitString):
        return {
            "pos": bs.read_vec16(),
            "scale": bs.read_float(constants["mapObjectMinScale"], constants["mapObjectMaxScale"], 8),
            "obj_type": bs.read_map_type(),
            "ori": bs.read_bits(2),
            "layer": bs.read_bits(2),
            "goreKills": bs.read_uint8()
        }

    @staticmethod
    def _obj_projectile_part(bs: TypedBitString):
        output = {
            "pos": bs.read_vec16(),
            "posZ": bs.read_float(0, constants["projectile"]["maxHeight"], 10),
            "dir": bs.read_unit_vec(7),
            "bombArmed": bs.read_bool()
        }

        bs.read_bits(7)
        return output

    @staticmethod
    def _obj_projectile_full(bs: TypedBitString):
        output = {
            "obj_type": bs.read_game_type(),
            "layer": bs.read_bits(2)
        }
        bs.read_bits(4)
        return output

    @staticmethod
    def _obj_smoke_part(bs: TypedBitString):
        return {
            "obj_type": bs.read_ascii_str(),
            "pos": bs.read_vec16(),
            "rad": bs.read_float(0, constants["smokeMaxRad"], 8)
        }

    @staticmethod
    def _obj_smoke_full(bs: TypedBitString):
        return {
            "obj_type": bs.read_ascii_str(),
            "layer": bs.read_bits(2),
            "interior": bs.read_bits(6)
        }

    @staticmethod
    def _obj_airdrop_part(bs: TypedBitString):
        return {
            "fallT": bs.read_float(0, 1, 7),
            "landed": bs.read_bool()
        }

    @staticmethod
    def _obj_airdrop_full(bs: TypedBitString):
        return {
            "pos": bs.read_vec16()
        }

    @staticmethod
    def _obj_npc_part(bs: TypedBitString):
        output = {
            "pos": bs.read_vec16(),
            "ori": bs.read_float(-4, 4, 8),
            "scale": bs.read_float(constants["mapObjectMinScale"], constants["mapObjectMaxScale"], 8),
            "state": bs.read_ascii_str(8),
            "invisibleTicker": bs.read_bool()
        }
        bs.read_align_to_next_byte()
        return output

    @staticmethod
    def _obj_npc_full(bs: TypedBitString):
        output = {
            "healthT": bs.read_float(0, 1, 8),
            "obj_type": bs.read_map_type(),
            "obstacleType": bs.read_ascii_str(),
            "layer": bs.read_bits(2),
            "dead": bs.read_bool(),
            "teamId": bs.read_uint8()
        }
        bs.read_align_to_next_byte()
        return output

    def decode_obj_part(self, obj):
        decoders = {
            0: self._obj_none_part,
            1: self._obj_player_part,
            2: self._obj_obstacle_part,
            3: self._obj_loot_part,
            4: self._obj_loot_spawner_part,
            5: self._obj_dead_body_part,
            6: self._obj_building_part,
            7: self._obj_structure_part,
            8: self._obj_decal_part,
            9: self._obj_projectile_part,
            10: self._obj_smoke_part,
            11: self._obj_airdrop_part,
            12: self._obj_npc_part
        }
        return decoders[obj["type"]](self.data)

    def decode_obj_full(self, obj):
        decoders = {
            0: self._obj_none_full,
            1: self._obj_player_full,
            2: self._obj_obstacle_full,
            3: self._obj_loot_full,
            4: self._obj_loot_spawner_full,
            5: self._obj_dead_body_full,
            6: self._obj_building_full,
            7: self._obj_structure_full,
            8: self._obj_decal_full,
            9: self._obj_projectile_full,
            10: self._obj_smoke_full,
            11: self._obj_airdrop_full,
            12: self._obj_npc_full
        }
        return decoders[obj["type"]](self.data)


class Type0aPacket(Packet):

    def encode(self, data):
        raise NotImplementedError("Type A packets should not be encoded client side")

    def decode(self, game_state):
        self.data.read_uint8()
        result = {
            "mapName": self.data.read_ascii_str(23),
            "seed": self.data.read_uint32(),
            "width": self.data.read_uint16(),
            "height": self.data.read_uint16(),
            "shoreInset": self.data.read_uint16(),
            "grassInset": self.data.read_uint16(),
            "rivers": [],
            "places": [],
            "objects": [],
            "groundPatches": []
        }

        river_count = self.data.read_uint8()
        for _ in range(river_count):
            result["rivers"].append(self.decode_river(self.data))

        place_count = self.data.read_uint8()
        for _ in range(place_count):
            result["places"].append(self.decode_place(self.data))

        object_count = self.data.read_uint16()
        for _ in range(object_count):
            result["objects"].append(self.decode_object(self.data))

        patch_count = self.data.read_uint8()
        for _ in range(patch_count):
            patch = self.decode_ground_patch(self.data)
            result["groundPatches"].append(patch)

        game_state.init_map(result)

        if log_xcodes:
            logger.debug("Decoded type A")
            logger.debug("In: " + str(self.data))
            logger.debug("Out: " + str(result))

    @staticmethod
    def decode_river(bs: TypedBitString):
        river = {
            "width": bs.read_bits(8),
            "looped": bs.read_uint8(),
            "points": []
        }
        point_count = bs.read_uint8()
        for _ in range(point_count):
            point = bs.read_vec16()
            river["points"].append(point)

        return river

    @staticmethod
    def decode_place(bs: TypedBitString):
        place = {
            "name": bs.read_ascii_str(),
            "pos": bs.read_vec16()
        }
        return place

    @staticmethod
    def decode_object(bs: TypedBitString):
        object_ = {
            "pos": bs.read_vec16(),
            "scale": bs.read_float(constants["mapObjectMinScale"], constants["mapObjectMaxScale"], 8),
            "type": bs.read_bits(12),
            "ori": bs.read_bits(2),
            "obstacleType": bs.read_ascii_str()
        }
        bs.read_bits(2)
        return object_

    @staticmethod
    def decode_ground_patch(bs: TypedBitString):
        result = {
            "min": bs.read_vec16(),
            "max": bs.read_vec16(),
            "colour": bs.read_uint32(),
            "roughness": bs.read_float32(),
            "offsetDist": bs.read_float32(),
            "order": bs.read_bits(7),
            "useAsMapShape": bs.read_bool()
        }
        return result


class GameConnection:
    def __init__(self, uri: str, join_packet_data: dict, version: int):
        """
        :param uri: uri of the game (or test) server
        :param join_packet_data: all of the data needed to make the first packet
        """

        update_constants()

        from survivpy_net.core import GameInstance, update_definitions
        update_definitions()

        self._loadout_stats = None
        self._quest_priv = None
        self._loadout_priv = None
        self._username = None
        self.version = version  # Communication protocol version
        self._settings = join_packet_data
        self._settings["protocol"] = self.version
        import queue
        self.message_queue = queue.Queue()
        self.decoded_queue = queue.Queue()
        del queue
        self._uri = uri
        self.EXIT = self.EXIT()
        self._ws = None
        self.state = GameInstance()
        self._sequence_num = 0
        self.last_packet_was_upwards = False

        from time import time
        self.t3_last_send_time = time()
        self.t3_last = {
            "moveLeft": False,
            "moveRight": False,
            "moveUp": False,
            "moveDown": False,
            "shootStart": False,
            "shootHold": False,
            "portrait": False,
            "touchMoveActive": False,
            "inputs": [],
            "useItem": ""
        }

        self._join()

    class EXIT:
        pass

    def send_message(self, message):
        """
        :param message: Any one of bytes, bytearray, packet or TypedBitString
        """
        if isinstance(message, (bytes, bytearray, BitString, Packet)):
            message = bytes(message)
        else:
            raise TypeError
        self._ws.send(message, True)
        self.last_packet_was_upwards = True

    def get_messages(self):
        messages = []
        while not self.message_queue.empty():
            messages.append(self.message_queue.get())
        return messages

    def get_decoded(self):
        messages = []
        while not self.decoded_queue.empty():
            messages.append(self.decoded_queue.get())
        return messages

    def send_input_msg(self, msg):
        if "seq" in msg:
            del msg["seq"]
        defaults = {
            "seq": 0,  # self._sequence_num,
            "moveLeft": False,
            "moveRight": False,
            "moveUp": False,
            "moveDown": False,
            "shootStart": False,
            "portrait": False,
            "touchMoveActive": False,
            "shootHold": False,
            "touchMoveDir": Vector(1, 0),
            "touchMoveLen": 255,
            "toMouseDir": Vector(1, 0),
            "toMouseLen": 0,
            "inputs": [],
            "useItem": "",
        }
        msg = defaults | msg
        packet = Type03Packet(msg)
        from time import time
        self.send_message(packet)
        self.t3_last_send_time = time()
        self.t3_last = msg

    def check_t3_timeout(self):
        from time import time
        if time() >= self.t3_last_send_time + 1:
            self.send_input_msg(self.t3_last)

    def _join(self):
        from ws4py.client.threadedclient import WebSocketClient

        exit_val = self.EXIT
        settings = self._settings
        m_queue = self.message_queue
        d_queue = self.decoded_queue
        state = self.state
        check_timeout = self.check_t3_timeout

        def get_lpwu():
            return self.last_packet_was_upwards

        def set_lpwu():
            self.last_packet_was_upwards = False

        def increment_seq():
            self._sequence_num = (self._sequence_num + 1) & 256

        class GameWebsocket(WebSocketClient):
            """
            Creates websocket connection to wss://[server]/play?gameId=[game_id]
            Sends messages from queue_in to server
            Sends messages from server to queue_out
            Adds EXIT to queue_out when connection is closed
            Closes connection if EXIT is on queue_in
            """

            def once(self):
                check_timeout()
                return super().once()

            def received_message(self, message):
                from math import ceil

                message = message.data
                if get_lpwu():
                    increment_seq()
                    set_lpwu()
                passes = 0
                byte_num = 0
                m_queue.put(message)
                while True:
                    if byte_num >= len(message):
                        break
                    packet_type = message[byte_num]
                    if not packet_type:
                        break
                        # Exit if null packet
                    decode_handlers = {
                        0x2: Type02Packet,
                        0x5: Type05Packet,
                        0x6: Type06Packet,
                        0xa: Type0aPacket
                    }

                    if packet_type not in decode_handlers:
                        return message

                    handler = decode_handlers[packet_type]
                    packet = handler(bytearray_data=message[byte_num:])
                    if isinstance(packet, Packet):
                        decoded = packet.decode(state)
                        if decoded:
                            d_queue.put(decoded)
                        byte_num = ceil(packet.data.index / 8) + byte_num
                    else:
                        break
                    passes += 1

            def opened(self):
                join_packet = Type01Packet(encode_data=settings)
                self.send(bytes(join_packet), True)

            def closed(self, code, reason=None):
                m_queue.put(exit_val)
                d_queue.put(exit_val)

        self._ws = GameWebsocket(self._uri)

        self._ws.daemon = True
        self._ws.connect()
