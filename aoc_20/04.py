import itertools
import re

from pydantic import BaseModel, ValidationError, validator
from typing import Optional, List, TypeVar, Type

from common import read_data


class Passport(BaseModel):
    eyr: int
    iyr: int
    byr: int
    ecl: str
    pid: str
    hcl: str
    hgt: str
    cid: Optional[int]


class ValidatedPassport(BaseModel):
    byr: int
    iyr: int
    eyr: int
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[int]

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
    lines = read_data("04", True)
    passports = []
    buffer_lines = []
    for line in lines:
        if line:
            buffer_lines.append(line)
        else:
            passport = parse_passport(buffer_lines, passport_type)
            if passport:
                passports.append(passport)
            buffer_lines.clear()
    return passports


def part_1():
    passports = parse_data(Passport)
    print(f"Total valid passports: {len(passports)}")


def part_2():
    passports = parse_data(ValidatedPassport)
    print(f"Total valid passports: {len(passports)}")


part_1()
part_2()
