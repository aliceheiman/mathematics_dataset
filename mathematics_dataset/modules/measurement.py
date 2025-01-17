# Copyright 2018 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Measurement questions, e.g., "How many hours are there in a day?"."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import functools
import random

# Dependency imports
from mathematics_dataset.util import lang
from mathematics_dataset import example
from mathematics_dataset.modules import train_test_split
from mathematics_dataset.sample import number
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import six
import sympy


def _make_modules(is_train):
    """Returns modules, with split based on the boolean `is_train`."""
    return {
        "conversion": functools.partial(conversion, is_train=is_train, is_extrapolation=False),
        "time": functools.partial(time, is_train=is_train),
    }


def train(entropy_fn):
    """Returns dict of training modules."""
    del entropy_fn  # unused
    return _make_modules(is_train=True)


def test():
    """Returns dict of testing modules."""
    return _make_modules(is_train=False)


def test_extra():
    """Returns dict of extrapolation testing modules."""
    return {
        "conversion": functools.partial(conversion, is_train=False, is_extrapolation=True),
    }


Unit = collections.namedtuple("Unit", ("name", "symbol"))


MICRO_SYMBOL = "u"

LENGTH = {
    Unit(lang.l.translate("meter"), "m"): 1,
    Unit(lang.l.translate("kilometer"), "km"): 1000,
    Unit(lang.l.translate("centimeter"), "cm"): sympy.Rational(1, 100),
    Unit(lang.l.translate("millimeter"), "mm"): sympy.Rational(1, 1000),
    Unit(lang.l.translate("micrometer"), "um"): sympy.Rational(1, 1e6),
    Unit(lang.l.translate("nanometer"), "nm"): sympy.Rational(1, 1e9),
}

TIME = {
    Unit(lang.l.translate("second"), "s"): 1,
    Unit(lang.l.translate("minute"), None): 60,
    Unit(lang.l.translate("hour"), None): 60 * 60,
    Unit(lang.l.translate("day"), None): 24 * 60 * 60,
    Unit(lang.l.translate("week"), None): 7 * 24 * 60 * 60,
    Unit(lang.l.translate("millisecond"), "ms"): sympy.Rational(1, 1e3),
    Unit(lang.l.translate("microsecond"), MICRO_SYMBOL + "s"): sympy.Rational(1, 1e6),
    Unit(lang.l.translate("nanosecond"), "ns"): sympy.Rational(1, 1e9),
}

TIME_YEARLY = {
    Unit(lang.l.translate("year"), None): 1,
    Unit(lang.l.translate("decade"), None): 10,
    Unit(lang.l.translate("century"), None): 100,
    Unit(lang.l.translate("millennium"), None): 1000,
    Unit(lang.l.translate("month"), None): sympy.Rational(1, 12),
}

MASS = {
    Unit(lang.l.translate("kilogram"), "kg"): 1,  # Yes, the *kilo*gram is the SI base unit.
    Unit(lang.l.translate("tonne"), "t"): 1000,
    Unit(lang.l.translate("gram"), "g"): sympy.Rational(1, 1e3),
    Unit(lang.l.translate("milligram"), "mg"): sympy.Rational(1, 1e6),
    Unit(lang.l.translate("microgram"), MICRO_SYMBOL + "g"): sympy.Rational(1, 1e9),
    Unit(lang.l.translate("nanogram"), "ng"): sympy.Rational(1, 1e12),
}

VOLUME = {
    Unit(lang.l.translate("litre"), "l"): 1,
    Unit(lang.l.translate("millilitre"), "ml"): sympy.Rational(1, 1000),
}


DIMENSIONS = [LENGTH, TIME, TIME_YEARLY, MASS, VOLUME]


def pluralize(name):

    # Plural mappings
    plurals = {
        lang.l.translate("meter"): lang.l.translate("meters"),
        lang.l.translate("kilometer"): lang.l.translate("kilometers"),
        lang.l.translate("centimeter"): lang.l.translate("centimeters"),
        lang.l.translate("millimeter"): lang.l.translate("millimeters"),
        lang.l.translate("micrometer"): lang.l.translate("micrometers"),
        lang.l.translate("nanometer"): lang.l.translate("nanometers"),
        lang.l.translate("second"): lang.l.translate("seconds"),
        lang.l.translate("minute"): lang.l.translate("minutes"),
        lang.l.translate("hour"): lang.l.translate("hours"),
        lang.l.translate("day"): lang.l.translate("days"),
        lang.l.translate("week"): lang.l.translate("weeks"),
        lang.l.translate("millisecond"): lang.l.translate("milliseconds"),
        lang.l.translate("microsecond"): lang.l.translate("microsecond"),
        lang.l.translate("nanosecond"): lang.l.translate("nanoseconds"),
        lang.l.translate("year"): lang.l.translate("years"),
        lang.l.translate("decade"): lang.l.translate("decades"),
        lang.l.translate("century"): lang.l.translate("centuries"),
        lang.l.translate("millennium"): lang.l.translate("millennia"),
        lang.l.translate("month"): lang.l.translate("months"),
        lang.l.translate("kilogram"): lang.l.translate("kilograms"),
        lang.l.translate("tonne"): lang.l.translate("tonnes"),
        lang.l.translate("gram"): lang.l.translate("grams"),
        lang.l.translate("milligram"): lang.l.translate("milligrams"),
        lang.l.translate("microgram"): lang.l.translate("micrograms"),
        lang.l.translate("nanogram"): lang.l.translate("nanograms"),
        lang.l.translate("litre"): lang.l.translate("litres"),
        lang.l.translate("millilitre"): lang.l.translate("millilitres"),
    }

    if name in plurals:
        return plurals[name]
    else:
        return name


def _factor_non_decimal(value):
    """Extras x dividing value such that x is coprime to 2 and 5."""
    result = 1
    factors = sympy.factorint(value)
    for factor, power in six.iteritems(factors):
        if factor not in [2, 5]:
            result *= factor ** power
    return result


def _sample_conversion_decimal(dimension, is_extrapolation):
    """Samples to and from units and values."""
    base_unit, target_unit = random.sample(list(dimension.keys()), 2)
    scale = sympy.Rational(dimension[base_unit]) / dimension[target_unit]
    scale_non_decimal = _factor_non_decimal(sympy.denom(scale))
    entropy = 9 if is_extrapolation else 7
    base_value = number.non_integer_decimal(entropy, signed=False)
    base_value = display.Decimal(base_value.value * scale_non_decimal)
    target_value = display.Decimal(base_value.value * scale)
    return base_value, base_unit, target_value, target_unit


def _conversion_decimal(context, is_train, is_extrapolation):
    """E.g., "How many grams are in 5kg?"."""
    dimension = random.choice(DIMENSIONS)
    while True:
        base_value, base_unit, target_value, target_unit = _sample_conversion_decimal(dimension, is_extrapolation)
        if train_test_split.is_train(base_value) == is_train:
            break

    templates = lang.l.parse(
        [
            "How many {target_name} [are there, fit, can fit] in {base_value} {base_name}?",
            "What is {base_value} {base_name} in {target_name}?",
            "[Convert, Rewrite, Transform, Translate] {base_value} {base_name} [to, into] {target_name}.",
            "[Write, Express] {base_value} {base_name} in {target_name}.",
            "Write {base_value} {base_name} expressed in {target_name}.",
        ]
    )
    if base_unit.symbol is not None:
        templates += lang.l.parse(
            [
                "How many {target_name} [are there, fit, can fit] in {base_value} {base_symbol}?",
                "What is {base_value} {base_symbol} in {target_name}?",
                "[Convert, Rewrite, Transform, Translate] {base_value} {base_symbol} [to, into] {target_name}.",
                "[Write, Express] {base_value} {base_symbol} in {target_name}.",
                "Write {base_value} {base_symbol} expressed in {target_name}.",
            ]
        )
    template = random.choice(templates)

    base_name = pluralize(base_unit.name)
    target_name = pluralize(target_unit.name)

    question = example.question(
        context,
        template,
        base_name=base_name,
        base_symbol=base_unit.symbol,
        base_value=base_value,
        target_name=target_name,
    )
    return example.Problem(question=question, answer=target_value)


def _conversion_fraction(context, is_train):
    """E.g., "How many grams are in three quarters of a kg?"."""
    dimension = random.choice(DIMENSIONS)

    # Limit probability of giving zero answer.
    allow_zero = random.random() < 0.2

    # Repeat until we find a pair with an integral answer. (Avoids ambiguity with
    # decimals.)
    while True:
        base_unit, target_unit = random.sample(list(dimension.keys()), 2)
        base_value = number.non_integer_rational(2, signed=False)
        if train_test_split.is_train(base_value) != is_train:
            continue
        answer = base_value * sympy.Rational(dimension[base_unit]) / sympy.Rational(dimension[target_unit])
        if abs(answer) <= 100000 and sympy.denom(answer) == 1 and (allow_zero or answer != 0):
            break

    template = random.choice(
        lang.l.parse(
            [
                "How many {target_name} [are there, fit, can fit] in {base_value} of a {base_name}?",
                "What is {base_value} of a {base_name} in {target_name}?",
                "[Write, Express] {base_value} of a {base_name} in {target_name}.",
            ]
        )
    )

    if sympy.denom(base_value) > 20 or random.choice([False, True]):
        base_value_string = base_value  # Will be represented as e.g., 2/3.
    else:
        base_value_string = display.StringNumber(base_value)  # e.g., two thirds

    question = example.question(
        context,
        template,
        base_name=base_unit.name,
        base_value=base_value_string,
        target_name=pluralize(target_unit.name),
    )
    return example.Problem(question=question, answer=answer)


def conversion(is_train, is_extrapolation):
    """Conversion question, in decimal or fraction."""
    context = composition.Context()
    # TODO(b/124038528): implement extrapolation for fraction conversions too
    if is_extrapolation or random.choice([False, True]):
        return _conversion_decimal(context, is_train=is_train, is_extrapolation=is_extrapolation)
    else:
        return _conversion_fraction(context, is_train=is_train)


def time(is_train):
    """Questions for calculating start, end, or time differences."""
    context = composition.Context()
    start_minutes = random.randint(1, 24 * 60 - 1)
    while True:
        duration_minutes = random.randint(1, 12 * 60 - 1)
        if train_test_split.is_train(duration_minutes) == is_train:
            break
    end_minutes = start_minutes + duration_minutes

    def format_12hr(minutes):
        """Format minutes from midnight in 12 hr format."""
        hours = (minutes // 60) % 24
        minutes %= 60
        am_pm = lang.l.translate("AM") if hours < 12 else lang.l.translate("PM")
        hours = (hours - 1) % 12 + 1
        return "{}:{:02} {}".format(hours, minutes, am_pm)

    start = format_12hr(start_minutes)
    end = format_12hr(end_minutes)

    which_question = random.randint(0, 3)
    if which_question == 0:
        # Question: What is start = end - duration?
        template = random.choice(
            lang.l.parse(
                [
                    "What time is it {duration} minutes before {end}?",
                    "What is the time {duration} minutes before {end}?",
                    "[Find, Work out, Compute, Calculate] the time {duration} minutes before {end}.",
                    "What was {end} {duration} minutes earlier?",
                ]
            )
        )
        return example.Problem(
            question=example.question(context, template, duration=duration_minutes, end=end), answer=start
        )
    elif which_question == 1:
        # Question: What is end = start + duration?
        template = random.choice(
            lang.l.parse(
                [
                    "What time is it {duration} minutes after {start}?",
                    "What is the time {duration} minutes after {start}?",
                    "[Find, Work out, Compute, Calculate] the time {duration} minutes after {start}.",
                    "What will {start} be {duration} minutes later?",
                ]
            )
        )
        return example.Problem(
            question=example.question(context, template, duration=duration_minutes, start=start), answer=end
        )
    else:
        # Question: What is duration = end - start?
        template = random.choice(
            lang.l.parse(
                [
                    "How many minutes [are there, fit, can fit] between {start} and {end}?",
                    "[Write, Work out, Compute, Calculate, Express, Find] the number of minutes between {start} and {end}.",
                ]
            )
        )
        return example.Problem(
            question=example.question(context, template, start=start, end=end), answer=duration_minutes
        )
