#!/bin/sh
# Tüm siteyi baştan üretir. Sıra önemli.
set -e
cd /home/claude/build
python3 make_payment.py --patch
python3 make_en.py
python3 make_workshops.py
python3 make_payment.py
python3 make_lang.py
