import itertools
import re
from typing import Optional, List, TypeVar, Type

from pydantic import BaseModel, ValidationError, validator

from common import read_line_groups


class Passport(BaseModel):
    eyr: int
    iyr: int
    byr: int
    ecl: str
    pid: str
    hcl: str
    hgt: str
    cid: Optional[int]


class ValidatedPassport(Passport):
    @validator('byr')
    def birth_year(cls, v):
        if not (1920 <= v <= 2002):
            raise ValueError('must be between 1920 and 2002')
        return v

    @validator('iyr')
    def issue_year(cls, v):
        if not (2010 <= v <= 2020):
            raise ValueError('must be between 2010 and 2020')
        return v

    @validator('eyr')
    def expiration_year(cls, v):
        if not (2020 <= v <= 2030):
            raise ValueError('must be between 2020 and 2030')
        return v

    @validator('hgt')
    def height(cls, v):
        unit_of_measure = v[-2:]
        amount = int(v[:-2])
        if unit_of_measure == "cm":
            if not (150 <= amount <= 193):
                raise ValueError(' value must be between 150 and 193')
        elif unit_of_measure == "in":
            if not (59 <= amount <= 76):
                raise ValueError(' value must be between 59 and 76')
        else:
            raise ValueError(' unit must be in or cm')
        return v

    @validator('hcl')
    def hair_color(cls, v):
        if not re.match(r"^#[0-9a-f]{6}$", v):
            raise ValueError('must be a RRGGBB color')
        return v

    @validator('ecl')
    def eye_color(cls, v):
        if v not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
            raise ValueError('must be a valid color')
        return v

    @validator('pid')
    def passport_id(cls, v):
        if not re.match(r"^[0-9]{9}$", v):
            raise ValueError('must be be a nine-digit number')
        return v


PassportType = TypeVar('PassportType')


def parse_passport(buffer_lines: List[str], passport_type: Type[PassportType]) -> Optional[PassportType]:
    raw_attributes = itertools.chain.from_iterable(line.split() for line in buffer_lines)
    attributes = {}
    for attribute in raw_attributes:
        k, v = attribute.split(":")
        attributes[k] = v

    try:
        passport = passport_type(**attributes)
    except ValidationError:
        passport = None

    return passport


def parse_data(passport_type: Type[PassportType]) -> List[PassportType]:
    line_groups = read_line_groups("04")
    all_passports = (parse_passport(line_group, passport_type) for line_group in line_groups)
    valid_passports = [passport for passport in all_passports if passport is not None]
    return valid_passports


def part_1(print_result: bool = True) -> int:
    passports = parse_data(Passport)
    valid_passports = len(passports)
    if print_result:
        print(f"Total valid passports: {valid_passports}")
    return valid_passports


def part_2(print_result: bool = True) -> int:
    passports = parse_data(ValidatedPassport)
    valid_passports = len(passports)
    if print_result:
        print(f"Total valid passports: {valid_passports}")
    return valid_passports


SOLUTION_1 = 256
SOLUTION_2 = 198

if __name__ == "__main__":
    part_1()
    part_2()
