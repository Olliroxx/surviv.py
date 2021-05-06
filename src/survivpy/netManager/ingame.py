class BitString:
    """
    Most of this is js translated to python, with some missing variable names
    """

    def __init__(self, buffer=None):
        """
        :param buffer: Input buffer, must be bytes, bytearray, list or tuple. (If using list/tuple, then all values must be positive integers below 256)
        """
        # TODO floats
        # TODO utf8 text

        if buffer is None:
            raise ValueError("Must have at least one of buffer and length")

        if type(buffer) not in (bytearray, tuple, list, bytes):
            raise TypeError("Input buffer must be byteArray")
        if type(buffer) in (tuple, list, bytes):
            buffer = bytearray(buffer)

        self._view = buffer

        self.index = 0

    def __len__(self):
        return len(self._view) * 8

    def __bytes__(self):
        return bytes(self._view)

    def _set_bit(self, offset, bit):
        if bit:
            self._view[offset >> 3] |= 1 << (offset & 7)
        else:
            self._view[offset >> 3] &= ~(1 << (offset & 7))

    def _get_bits(self, offset, length, return_is_positive=False):
        remaining = len(self._view) * 8 - offset
        if length > remaining:
            raise ValueError("Cannot get " + str(length) + " bit(s) from offset " + str(offset) + ", " + str(remaining) + " available")

        unknown_1 = 0
        i = 0
        while i < length:
            left = length - i
            masked_offset = offset & 7
            byte = self._view[offset >> 3]
            size = min(left, 8 - masked_offset)
            unknown_2 = (1 << size) - 1
            unknown_3 = byte >> masked_offset & unknown_2

            unknown_1 = unknown_1 | unknown_3 << i
            offset = offset + size
            i = i + size

        if return_is_positive:
            return length != 32 & unknown_1 & 1 << length - 1 & unknown_1 - 1, unknown_1
        return unknown_1

    def _set_bits(self, offset, bits, length):
        free = len(self._view) * 8 - offset
        if length > free:
            raise ValueError(
                "Cannot set " + str(length) + " bit(s) from offset " + str(offset) + ", " + str(free) + " available")

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

    def _get_float8(self, offset):
        max_value = 255
        bits = self._get_bits(offset, 8)
        coefficient = bits / max_value
        return 0.125 + coefficient * 2.375

    def _get_float16(self, offset):
        max_value = 65536
        bits = self._get_bits(offset, 16)
        coefficient = bits / max_value
        return coefficient * 1024

    def _get_float32(self, offset):
        bits = self._get_bits(offset, 32).to_bytes(4, "big")
        import struct
        return struct.unpack(">f", bits)

    def _get_float64(self, offset):
        bits = self._get_bits(offset, 64).to_bytes(8, "big")
        import struct
        return struct.unpack(">d", bits)

    def _set_bool(self, offset, boolean):
        self._set_bits(offset, int(boolean), 1)

    def _set_int8(self, offset, int8):
        self._set_bits(offset, int8, 8)

    def _set_uint8(self, offset, uint8):
        self._set_bits(offset, uint8, 8)

    def _set_int16(self, offset, int16):
        self._set_bits(offset, int16, 16)

    def _set_uint16(self, offset, uint16):
        self._set_bits(offset, uint16, 16)

    def _set_int32(self, offset, int32):
        self._set_bits(offset, int32, 32)

    def _set_uint32(self, offset, uint32):
        self._set_bits(offset, uint32, 32)

    def _set_float32(self, offset, float32):
        import struct
        packed = struct.pack(">f", float32)
        self._set_bits(offset, int.from_bytes(packed, "big"), 32)
        # TODO check if correct endian
        # TODO check if int or uint

    def _set_float64(self, offset, float64):
        pass

    def _get_array_buffer(self, offset, elements):
        result = list(elements)

        i = 0
        while i < elements:
            result[i] = self._get_uint8(offset + i * 8)
            i += 1

    def read_ascii_str(self, length=None):
        return self._read_str(self, length, False)

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
            length += 1  # Minor difference in implementation, means this is necessary

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
            pass  # TODO
        else:
            return str_trim

    @staticmethod
    def _write_ascii_string(bitstring, string):

        for char in string:
            bitstring.write_uint8(ord(char))
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

    def read_float8(self):
        result = self._get_float8(self.index)
        self.index += 8
        return result

    def read_float16(self):
        result = self._get_float16(self.index)
        self.index += 16
        return result

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
    
    def read_vec8(self):
        x = self.read_float8()
        y = self.read_float8()
        result = (x, y)
        return result
    
    def read_vec16(self):
        x = self.read_float16()
        y = self.read_float16()
        result = (x, y)
        return result
    
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

    def write_float64(self, float64):
        self._set_float64(self.index, float64)
        self.index += 64

    def write_ascii_str(self, text: str):
        self._write_ascii_string(self, text)

    def write_utf8_str(self, text: str):
        self._write_utf8_string(self, text)

    def bits_free(self):
        return len(self) - self.index

    def extend(self, amount: int):
        if type(amount) != int:
            raise ValueError("Amount must be int")

        if amount > 0:
            raise ValueError("Amount must be greater than 0 ")

        self._view[-1:] = [0] * amount

    def align_to_next_byte(self):
        self._view = self._view.rstrip(b"\x00") + b"\x00"


class Packet:
    def __init__(self, encode_data=None, bytearray_data=None):

        self.constants = {
                    'MapNameMaxLen': 0x18,
                    'PlayerNameMaxLen': 0x10,
                    'MouseMaxDist': 0x40,
                    'SmokeMaxRad': 0xa,
                    'ActionMaxDuration': 0xc,
                    'AirstrikeZoneMaxRad': 0x100,
                    'AirstrikeZoneMaxDuration': 0x3c,
                    'PlayerMinScale': 0.75,
                    'PlayerMaxScale': 0x2,
                    'MapObjectMinScale': 0.125,
                    'MapObjectMaxScale': 2.5,
                    'MaxPerks': 0x8,
                    'MaxMapIndicators': 0x10
                }

        self.decoded = None

        if bytearray_data is not None:
            if type(bytearray_data) in (bytes, bytearray):
                self.data = BitString(bytearray_data)
            elif type(bytearray_data) == str:
                self.data = BitString(bytearray.fromhex(bytearray_data))
            else:
                raise ValueError("Invalid data type " + str(type(bytearray_data)))
            self.decode()
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

    def decode(self):
        raise NotImplementedError("This should be overridden")


class Type01Packet(Packet):

    def encode(self, fields):
        self.data = BitString(bytearray(17 * 1024))
        self.data.write_uint8(1)
        self.data.write_uint32(fields["protocol"])
        self.data.write_ascii_str(fields["matchPriv"])
        self.data.write_ascii_str(fields["loadoutPriv"])
        self.data.write_ascii_str(fields["loadoutStats"])
        self.data.write_bool(fields["hasGoldenBP"])
        self.data.write_ascii_str(fields["questPriv"])
        self.data.write_ascii_str(fields["name"])
        self.data.write_bool(fields["isUnlinked"])
        self.data.write_bool(fields["useTouch"])
        self.data.write_bool(fields["isMobile"])
        self.data.write_bool(fields["proxy"])
        self.data.write_bool(fields["otherProxy"])
        self.data.write_bool(fields["bot"])
        self.data.write_bool(fields["autoMelee"])
        self.data.write_bool(fields["aimAssist"])
        self.data.write_ascii_str(fields["kpg"])
        self.data.align_to_next_byte()

    def decode(self):
        raise NotImplementedError("Type 1 packets should not be decoded client side")


class Type02Packet(Packet):

    def encode(self, data):
        raise NotImplementedError("Type 2 packets should not be encoded client side")

    def decode(self):
        result = {
            "reason": self.data.read_ascii_str()
        }
        return result


class Type0aPacket(Packet):

    def encode(self, data):
        raise NotImplementedError("Type 5 packets should not be encoded client side")

    def decode(self):
        result = {
            "mapName": self.data.read_ascii_str(self.constants["MapNameMaxLen"]),
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
            result["groundPatches"].append(self.decode_ground_patches(self.data))

        self.decoded = result

    @staticmethod
    def decode_river(bitstring):
        river = {
            "width": bitstring.read_bits(8),
            "looped": bitstring.read_uint8(),
            "points": []
        }
        point_count = bitstring.read_uint8()
        for _ in range(point_count):
            point = bitstring.read_vec16()
            river["points"].append(point)

        return river

    @staticmethod
    def decode_place(bitstring):
        place = {
            "name": bitstring.read_ascii_str(),
            "pos": bitstring.read_vec16()
        }
        return place

    @staticmethod
    def decode_object(bitstring):
        object_ = {
            "pos": bitstring.read_vec16(),
            "scale": bitstring.read_float8(),
            "type": bitstring.read_bits(12),
            "ori": bitstring.read_bits(2),
            "obstacleType": bitstring.read_ascii_str()
        }
        bitstring.read_bits(2)
        return object_

    @staticmethod
    def decode_ground_patches(bitstring):
        result = {
            "min": bitstring.read_vec16(),
            "max": bitstring.read_vec16(),
            "colour": bitstring.read_uint32(),
            "roughness": bitstring.read_uint32(),
            "offsetDist": bitstring.read_uint32(),
            "order": bitstring.read_bits(7),
            "useAsMapShape": bitstring.read_bool()
        }
        return result


class Game(object):
    def __init__(self, uri, join_packet_data, version):
        """
        :param uri: uri of the game (or test) server
        :param join_packet_data: all of the data needed to make the first packet
        """
        self._loadout_stats = None
        self._quest_priv = None
        self._loadout_priv = None
        self._username = None
        self.version = version  # Communication protocol version
        self._settings = join_packet_data
        self._settings["protocol"] = self.version
        import queue
        self._queue_soci = queue.Queue()
        del queue
        self._uri = uri
        self.EXIT = self.EXIT()
        self.ws = None
        self._join()

    class EXIT:
        pass

    def _autodecode_packet(self, packet):
        if packet == self.EXIT:
            return packet

        decode_handlers = {
            0x2: Type02Packet,
            0xa: Type0aPacket
        }

        if packet[0] not in decode_handlers:
            return packet

        handler = decode_handlers[packet[0]]
        packet = handler(bytearray_data=packet)

        return packet.decoded

    def send_message(self, message, is_binary):
        self.ws.send(message, is_binary)

    def get_decoded_messages(self):
        messages = []
        while not self._queue_soci.empty():
            message = self._queue_soci.get()
            decoded = self._autodecode_packet(message)
            messages.append(decoded)
        return messages

    def _join(self):
        from ws4py.client.threadedclient import WebSocketClient

        exit_val = self.EXIT

        settings = self._settings

        queue = self._queue_soci

        class game_websocket(WebSocketClient):
            """
            Creates websocket connection to wss://[server]/play?gameId=[game_id]
            Sends messages from queue_in to server
            Sends messages from server to queue_out
            Adds EXIT to queue_out when connection is closed
            Closes connection if EXIT is on queue_in
            """

            def received_message(self, message):
                queue.put(message.data)

            def opened(self):
                join_packet = Type01Packet(encode_data=settings)
                self.send(bytes(join_packet), True)

            def closed(self, code, reason=None):
                queue.put(exit_val)

            def ponged(self, pong):
                print("Ponged: " + str(pong))

        self.ws = game_websocket(self._uri)

        self.ws.connect()
        self.ws.run_forever()


if __name__ == '__main__':
    pass
