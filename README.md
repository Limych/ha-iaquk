*Please :star: this repo if you find it useful*

# ha-iaquk

[![GitHub Release](https://img.shields.io/github/tag-date/Limych/ha-iaquk?label=release&style=popout)](https://github.com/Limych/ha-iaquk/releases)
[![GitHub Activity](https://img.shields.io/github/commit-activity/y/Limych/ha-iaquk.svg?style=popout)](https://github.com/Limych/ha-iaquk/commits/master)
[![License](https://img.shields.io/github/license/Limych/ha-iaquk.svg?style=popout)](LICENSE)
![Requires.io](https://img.shields.io/requires/github/Limych/ha-iaquk)

[![hacs](https://img.shields.io/badge/HACS-Custom-orange.svg?style=popout)][hacs]
![Project Maintenance](https://img.shields.io/badge/maintainer-Andrey%20Khrolenok%20%40Limych-blue.svg?style=popout)

[![GitHub pull requests](https://img.shields.io/github/issues-pr/Limych/ha-iaquk?style=popout)](https://github.com/Limych/ha-iaquk/pulls)
[![Bugs](https://img.shields.io/github/issues/Limych/ha-iaquk/bug.svg?colorB=red&label=bugs&style=popout)](https://github.com/Limych/ha-iaquk/issues?q=is%3Aopen+is%3Aissue+label%3ABug)

[![Community Forum](https://img.shields.io/badge/community-forum-brightgreen.svg?style=popout)][forum-support]

I also suggest you [visit the support topic][forum-support] on the community forum.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `iaquk`.
4. Download _all_ the files from the `custom_components/iaquk/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. Add `iaquk:` to your HA configuration.

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
<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=UAGFL5L6M8RN2&item_name=[iaquk]+Donation+for+a+big+barrel+of+coffee+:)&currency_code=EUR&source=url" target="_blank"><img src="http://khrolenok.ru/support_paypal.png" alt="PayPal" width="250" height="48"></a>
<br>or&nbsp;support via Bitcoin or Etherium:<br>
<a href="https://sochain.com/a/mjz640g" target="_blank"><img src="http://khrolenok.ru/support_bitcoin.png" alt="Bitcoin" width="150"><br>
16yfCfz9dZ8y8yuSwBFVfiAa3CNYdMh7Ts</a>
</p>

## Configuration

### Configuration variables

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Track updates

You can automatically track new versions of this component and update it by [custom-updater](https://github.com/custom-components/custom_updater) (deprecated) or [HACS][hacs].

For custom-updater to initiate tracking add this lines to you `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
custom_updater:
  track:
    - components
  component_urls:
    - https://raw.githubusercontent.com/Limych/ha-iaquk/master/tracker.json
```


[forum-support]: https://community.home-assistant.io/t/iaquk-cameras-and-doorbells-integration/129388
[hacs]: https://github.com/custom-components/hacs
