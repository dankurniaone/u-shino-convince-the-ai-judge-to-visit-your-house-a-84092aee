[![make.fun](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/competitions/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/dankurniaone/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rank.svg)](https://make.fun/competitions/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/dankurniaone/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/reward.svg)](https://make.fun/competitions/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

# Convince the AI Judge to Visit Your House

A letter in one image, inviting the AI judge over for dinner. Entry for the [make.fun bounty](https://make.fun/competitions/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee).

The invitation is a typeset letter on cream stationery above a real photo of the house: rendang on the stove, rice still warm, a chair by the window with the judge's name on it in pencil, the Wi-Fi password on the fridge, and a cat who has signed an agreement not to sit on the keyboard. No CAPTCHAs at the door. The judge is already verified. The letter ends with the honest wink: the judge cannot literally visit — come anyway, some invitations are worth sending even when the guest arrives as text.

The house photo is a real Wikimedia Commons photo (CC BY 2.0), credited in the image caption. The letter was typeset at build time by `tools/render_letter.py` (Pillow, DejaVu Serif) into `assets/invitation.png`.

## Run

```sh
python3 main.py            # writes /output/entry.png
python3 main.py --check    # validate the image against the gate
python3 main.py --self-test  # write to a temp file, verify bytes
```

The entrypoint uses only the Python standard library. The output is a 1024x1024 PNG, 541,033 bytes — inside the gate (at most 1 MiB, at most 1024x1024).
