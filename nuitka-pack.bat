python -m nuitka --windows-disable-console --standalone --follow-import-to=core --windows-icon-from-ico=icon.ico --windows-file-version=1.1.0.18 --windows-product-name="Boss Key" --windows-file-description="Boss Key Application" --include-data-file=icon.ico=. --windows-company-name="Ivan Hanloth" --show-progress --mingw64 --copyright="Copyright (C) 2024 Ivan Hanloth All Rights Reserved. " --output-dir=out Boss-Key.py
pause