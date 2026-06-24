# FAIC Game Controller

FAIC Game Controller la desktop app dung webcam de dieu khien game dua xe bang cu chi tay. App khong phai game doc lap; no nhan dien hai tay qua camera, tinh goc nhu vo lang ao, roi gia lap phim `W/A/S/D/Space` vao Windows de dieu khien game ben ngoai nhu Asphalt 8.

App duoc thiet ke cho demo TechFest: co giao dien desktop, camera preview, HUD tren frame camera, nut Start/Pause/Stop/Emergency Stop va man hinh Settings.

## Project nay lam gi?

- Bien hai tay thanh vo lang ao.
- Gui phim dieu khien vao game dua xe dang focus.
- Hien thi camera preview truc tiep trong app.
- Hien thi action hien tai, goc lai, phim dang bam, FPS va so tay detect duoc.
- Cho phep chinh config co ban trong UI.

## Tinh nang chinh

- Desktop UI bang CustomTkinter.
- Racing Controller co camera preview va panel trang thai.
- Input Manager co cache trang thai phim, khong spam press/release moi frame.
- Camera worker chay thread rieng, khong block UI.
- Config luu trong `config.json`.
- HUD TechFest neon tren frame camera.
- Emergency Stop de release tat ca phim ngay lap tuc.

## Demo flow

1. Mo game dua xe, vi du Asphalt 8.
2. Chay `start.bat` hoac `python main.py`.
3. Trong app, chon `Racing Controller`.
4. Bam `Start`.
5. Dua hai tay len truoc camera.
6. Click lai vao cua so game neu game chua nhan phim.
7. Dung `Pause`, `Stop` hoac `Emergency Stop` khi can.

## Cau truc thu muc

```text
FAICGame_HomeComing/
|-- main.py
|-- config.json
|-- requirements.txt
|-- setup.bat
|-- run.bat
|-- start.bat
|-- core/
|   |-- config_manager.py
|   |-- hand_tracker.py
|   |-- racing_logic.py
|   |-- input_manager.py
|   |-- hud_renderer.py
|   `-- camera_worker.py
|-- ui/
|   |-- app.py
|   |-- home_frame.py
|   |-- racing_frame.py
|   `-- settings_frame.py
|-- legacy/
|   |-- README.md
|   |-- pointerGameController.py
|   |-- leftHolderMouseButton.py
|   `-- SteeringWheelDisplay.py
|-- CarGameController.py
|-- keyinput.py
`-- skills-lock.json
```

## Yeu cau he thong

- Windows.
- Webcam.
- Python 3.10 khuyen dung.
- Game dua xe co ho tro ban phim.

Khuyen nghi dung Python 3.10 vi MediaPipe co the loi voi Python qua moi.

## Cai dat nhanh

Double click:

```text
start.bat
```

Neu chua co `.venv`, `start.bat` se goi `setup.bat` de tao moi truong va cai dependencies.

## Chay nhanh

Neu da setup:

```text
run.bat
```

Hoac:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

## Chay thu cong

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Neu PowerShell chan activate script:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Cach dung Racing Controller

- `Start`: mo camera, detect tay, render HUD va gui phim vao Windows.
- `Pause / Resume`: tam dung hoac tiep tuc gui phim. Khi pause, app release tat ca phim dang giu.
- `Stop`: dung camera worker, release tat ca phim va xoa preview.
- `Emergency Stop`: release ngay tat ca phim `W/A/S/D/Space`.
- `Back to Home`: quay ve Home, worker se duoc cleanup.

Khi dong app, app cung release tat ca phim va giai phong camera.

## Gesture

| Gesture | Phim | Y nghia |
| --- | --- | --- |
| Hai tay nhu cam vo lang | `W` | Chay toi |
| Nghieng tay sang trai | `A` | Re trai |
| Nghieng tay sang phai | `D` | Re phai |
| Nang hai tay len vung tren | `Space` | Boost/Nitro |
| Ha hai tay xuong vung duoi | `S` | Drift/Brake |
| Ha hai tay va nghieng trai/phai | `S` + `A/D` | Drift trai/phai |
| Khong du 2 tay | Tha phim | Dung dieu khien |

## Settings va config

Settings luu vao `config.json`.

Co the chinh:

- Camera index.
- Camera width/height.
- Steering threshold.
- Drift steering threshold.
- Boost zone ratio.
- Drift zone ratio.
- Show landmarks.
- Show FPS.

Neu thay doi camera index/resolution khi camera dang chay, hay `Stop` roi `Start` lai de ap dung chac chan.

## Loi thuong gap

### Khong mo duoc camera

- Kiem tra camera co dang bi app khac dung khong.
- Thu doi Camera index trong Settings: `0`, `1`, `2`.
- Rut/cam lai webcam neu dung webcam roi.

### MediaPipe loi do Python version

Dung Python 3.10 va cai lai:

```powershell
Remove-Item -Recurse -Force .venv
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Game khong nhan phim

- Click vao cua so game de focus.
- Chay game o windowed/borderless mode neu can.
- Dam bao game dung phim `W/A/S/D/Space`.
- Mot so game can chay app voi quyen phu hop de nhan input.

### App bi lag

- Dung camera `640x480`.
- Tat `Show landmarks`.
- Dong app khac dang dung camera.
- Dam bao phong du sang.

### Camera bi nguoc

Preview dang flip ngang de giong guong soi. Neu muon doi, sua dong `cv2.flip(frame, 1)` trong `core/camera_worker.py`.

## Khuyen nghi demo

- Dung Python 3.10.
- Dung camera 640x480 de giam lag.
- Chay game o windowed/borderless mode.
- Dat camera ngang tam nguc hoac mat.
- Nen co anh sang tot va nen sau lung don gian.

## Roadmap

- Calibration nang cao cho tung nguoi choi.
- Nhieu HUD theme.
- Dong goi thanh file `.exe`.
