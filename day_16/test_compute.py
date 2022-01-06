import pytest

from day_16.compute import PacketHeader, TypeID, LiteralValue, HexSource, Operator, q1_version_sum, Packet, q2_process


class TestPacketHeader:

    @pytest.mark.parametrize('hex_src, expected, left_over', (
        (HexSource('D2'), PacketHeader(6, TypeID.LiteralValue), '10'),
        (HexSource('38'), PacketHeader(1, TypeID.LessThan), '00'),
        (HexSource('40', _left_over_binary='01'), PacketHeader(2, TypeID.LiteralValue), ''),
    ))
    def test_from_str(self, hex_src: HexSource, expected: PacketHeader, left_over: str):
        assert PacketHeader.from_str(hex_src) == expected
        assert hex_src._left_over_binary == left_over


class TestLiteralValue:

    @pytest.mark.parametrize('hex_src, expected, left_over', (
        (HexSource('D2FE28'), LiteralValue(PacketHeader(6, TypeID.LiteralValue), 2021), '000'),
        (HexSource('307'), LiteralValue(PacketHeader(1, TypeID.LiteralValue), 3), '1'),
    ))
    def test_from_str(self, hex_src: HexSource, expected: LiteralValue, left_over: str):
        assert LiteralValue.from_src(hex_src) == expected
        assert hex_src._left_over_binary == left_over


class TestOperator:

    @pytest.mark.parametrize('hex_src, expected, left_over', (
        (
            HexSource('38006F45291200'),
            Operator(
                PacketHeader(1, TypeID.LessThan),
                packet_content=[
                    LiteralValue(PacketHeader(6, TypeID.LiteralValue), 10),
                    LiteralValue(PacketHeader(2, TypeID.LiteralValue), 20),
                ],
            ),
            '000',
        ),
        (
            HexSource('EE00D40C823060'),
            Operator(
                PacketHeader(7, TypeID.Maximum),
                packet_content=[
                    LiteralValue(PacketHeader(2, TypeID.LiteralValue), 1),
                    LiteralValue(PacketHeader(4, TypeID.LiteralValue), 2),
                    LiteralValue(PacketHeader(1, TypeID.LiteralValue), 3),
                ],
            ),
            '0'
        ),
        (
            HexSource('8A004A801A8002F478'),
            Operator(
                PacketHeader(4, TypeID.Minimum),
                packet_content=[
                    Operator(
                        PacketHeader(1, TypeID.Minimum),
                        packet_content=[
                            Operator(
                                PacketHeader(5, TypeID.Minimum),
                                packet_content=[
                                    LiteralValue(
                                        PacketHeader(6, TypeID.LiteralValue),
                                        15,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            '000'
        ),
    ))
    def test_from_str(self, hex_src: HexSource, expected: Operator, left_over: str):
        assert Operator.from_src(hex_src) == expected
        assert hex_src._left_over_binary == left_over

    @pytest.mark.parametrize('source, expected', (
        ('38006F45291200', 9),
        ('8A004A801A8002F478', 16),
        ('620080001611562C8802118E34', 12),
        ('C0015000016115A2E0802F182340', 23),
        ('A0016C880162017C3686B18A3D4780', 31),
    ))
    def test_version_sum(self, source: str, expected: int):
        op = Operator.from_src(HexSource(source))
        assert op.version_sum() == expected

    @pytest.mark.parametrize('source, expected', (
        ('C200B40A82', 3),  # sum(1, 2)
        ('04005AC33890', 54),  # prod(6, 9)
        ('880086C3E88112', 7),  # min(7, 8, 9)
        ('CE00C43D881120', 9),  # max(7, 8, 9)
        ('D8005AC2A8F0', 1),  # 5 < 15
        ('F600BC2D8F', 0),  # 5 > 15
        ('9C005AC2F8F0', 0),  # 5 == 15
        ('9C0141080250320F1802104A08', 1)  # 1 + 3 == 2 * 2
    ))
    def test_process(self, source: str, expected: int):
        assert Operator.from_src(HexSource(source)).process() == expected


def test_q1():
    assert q1_version_sum(Packet.from_file('input.txt')) == 906


def test_q2():
    assert q2_process(Packet.from_file('input.txt')) == [819324480368]