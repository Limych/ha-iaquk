*Please :star: this repo if you find it useful*

# Indoor Air Quality Sensor Component for Home Assistant

[![GitHub Release](https://img.shields.io/github/tag-date/Limych/ha-iaquk?label=release&style=popout)](https://github.com/Limych/ha-iaquk/releases)
[![GitHub Activity](https://img.shields.io/github/commit-activity/y/Limych/ha-iaquk.svg?style=popout)](https://github.com/Limych/ha-iaquk/commits/master)
[![License](https://img.shields.io/github/license/Limych/ha-iaquk.svg?style=popout)](LICENSE)
![Requires.io](https://img.shields.io/requires/github/Limych/ha-iaquk)

[![hacs](https://img.shields.io/badge/HACS-Default-orange.svg?style=popout)][hacs]
![Project Maintenance](https://img.shields.io/badge/maintainer-Andrey%20Khrolenok%20%40Limych-blue.svg?style=popout)

[![GitHub pull requests](https://img.shields.io/github/issues-pr/Limych/ha-iaquk?style=popout)](https://github.com/Limych/ha-iaquk/pulls)
[![Bugs](https://img.shields.io/github/issues/Limych/ha-iaquk/bug.svg?colorB=red&label=bugs&style=popout)](https://github.com/Limych/ha-iaquk/issues?q=is%3Aopen+is%3Aissue+label%3ABug)

[![Community Forum](https://img.shields.io/badge/community-forum-brightgreen.svg?style=popout)][forum-support]

This component allows you to evaluate the air quality in any room, using data from various sensors installed there. Such as temperature, humidity, carbon dioxide sensors, etc.

The index is calculating in accordance with the [IAQ UK organization methodology](IAQ_Rating_Index.pdf).

I also suggest you [visit the support topic][forum-support] on the community forum.

![](iaquk.jpg)

## Installation

### HACS - Recommended

1. Have [HACS](https://hacs.xyz) installed, this will allow you to easily manage and track updates.
1. Search for "Indoor Air Quality UK Index".
1. Click Install below the found integration.
1. Configure using the configuration instructions below.
1. Restart Home-Assistant.

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `iaquk`.
4. Download _all_ the files from the `custom_components/iaquk/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
1. Configure using the configuration instructions below.
1. Restart Home-Assistant.

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/iaquk/__init__.py
custom_components/iaquk/const.py
custom_components/iaquk/manifest.json
custom_components/iaquk/sensor.py
```

<p align="center">* * *</p>
I put a lot of work into making this repo and component available and updated to inspire and help others! I will be glad to receive thanks from you — it will give me new strength and add enthusiasm:
<p align="center"><br>
<a href="https://www.patreon.com/join/limych?" target="_blank"><img src="http://khrolenok.ru/support_patreon.png" alt="Patreon" width="250" height="48"></a>
<br>or&nbsp;support via Bitcoin or Etherium:<br>
<a href="https://sochain.com/a/mjz640g" target="_blank"><img src="http://khrolenok.ru/support_bitcoin.png" alt="Bitcoin" width="150"><br>
16yfCfz9dZ8y8yuSwBFVfiAa3CNYdMh7Ts</a>
</p>

## Usage

To use this component in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
iaquk:
  kitchen:
    sources:
      temperature: sensor.kitchen_temperature
      humidity: sensor.kitchen_humidity
      co2: sensor.kitchen_eco2
      tvoc: sensor.kitchen_tvoc
    sensors:
      - iaq_level

  livingroom:
    name: "Living Room"
    sources:
      hcho: sensor.livingroom_formaldehyde
      pm:
        - sensor.livingroom_pm25
        - sensor.livingroom_pm10
```

### Configuration variables

Each room in the settings is defined by its own named group of parameters. You can specify the friendly name of this group (room), the sensors involved in the calculations, and which sensors you need to create for the output.

You can create as many groups as you need. But each group must have an unique name.

**name**:\
  _(string) (Optional)_\
  Friendly name to use in the frontend.\
  _Default value: deslugified group name_

**sources**:\
  _(dictionary) (Required)_\
  Dictionary of sensors involved in the calculations. At least one sensor must be specified.

> **temperature**:\
> _(string) (Optional)_\
> Room temperature sensor entity ID.\
> Required sensor's unit of measurement: °C or °F
>
> **humidity**:\
> _(string) (Optional)_\
> Room humidity sensor entity ID.\
> Required sensor's unit of measurement: %
>
> **co2**:\
> _(string) (Optional)_\
> Room Carbon Dioxide (CO<sub>2</sub>) sensor entity ID.\
> Required sensor's unit of measurement: ppm, ppb, mg/m<sup>3</sup> or µg/m<sup>3</sup>
>
> **co**:\
> _(string) (Optional)_\
> Room Carbon Monoxide (CO) sensor entity ID.\
> Required sensor's unit of measurement: ppm, ppb, mg/m<sup>3</sup> or µg/m<sup>3</sup>
>
> **no2**:\
> _(string) (Optional)_\
> Room Nitrogen Dioxide (NO<sub>2</sub>) sensor entity ID.\
> Required sensor's unit of measurement: ppm, ppb, mg/m<sup>3</sup> or µg/m<sup>3</sup>
>
> **tvoc**:\
> _(string) (Optional)_\
> Room tVOC sensor entity ID.\
> Required sensor's unit of measurement: ppm, ppb, mg/m<sup>3</sup> or µg/m<sup>3</sup>
>
> **hcho**:\
> _(string) (Optional)_\
> Room Formaldehyde (HCHO; CH<sub>2</sub>O) sensor entity ID.\
> Required sensor's unit of measurement: ppm, ppb, mg/m<sup>3</sup> or µg/m<sup>3</sup>
>
> **radon**:\
> _(string) (Optional)_\
> Room Radon (Rn) sensor entity ID.\
> Required sensor's unit of measurement: Bq/m<sup>3</sup>
>
> **pm**:\
> _(string | list) (Optional)_\
> Room particulate matter sensors entity IDs.\
> Required sensor's unit of measurement: mg/m<sup>3</sup> or µg/m<sup>3</sup>

**sensors**:\
  _(list) (Optional)_\
  List of sensors  you need to create for the output. The following sensors can be added:\
  _Default value: all sensors below_

> **iaq_index**:\
> The sensor displays the air quality in numerical form from 1 to 65. The higher the value, the better the air quality.
>
> **iaq_level**:\
> The sensor shows the air quality in a human-readable form. Possible values: Excellent, Good, Fair, Poor, Inadequate.

**_Note_**:\
The icon of `iaq_level` sensor changes its image depending on the value of the sensor.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Track updates

You can automatically track new versions of this component and update it by [HACS][hacs].

## License

MIT License

Copyright (c) 2019–2020 Andrey "Limych" Khrolenok

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[forum-support]: https://community.home-assistant.io/t/indoor-air-quality-sensor-component/160474
[hacs]: https://github.com/custom-components/hacs
