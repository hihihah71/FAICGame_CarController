# FAIC Game HomeComing

Project nay la bo dieu khien game dua xe bang cu chi tay qua webcam. Ung dung se nhan dien hai tay, xem hai tay nhu dang cam vo lang ao, sau do gia lap cac phim `W`, `A`, `S`, `D`, `Space` de dieu khien game dang mo tren may.

Project phu hop de demo AI/computer vision trong TechFest/FAIC. No khong phai la game doc lap, vi vay ban can mo mot game dua xe rieng, vi du Asphalt 8.

## Tinh nang

- Nhan dien hai tay bang webcam.
- Tinh goc nghieng giua hai tay de re trai/phai.
- Gia lap phim dieu khien xe tren Windows.
- Ho tro vung BOOST va DRIFT bang vi tri hai tay.
- Co cac module phu de dieu khien chuot bang cu chi tay.

## Yeu cau

- Windows.
- Webcam.
- Python 3.10 hoac 3.11 khuyen dung.
- Game dua xe co ho tro ban phim, vi du Asphalt 8.

Luu y: Python 3.13 co the gap loi voi MediaPipe API cu. Neu gap loi `mediapipe` khong co `solutions`, hay dung Python 3.10.

## Cai dat

Mo PowerShell tai thu muc project:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Neu PowerShell chan file activate voi loi `execution of scripts is disabled`, chay:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Sau do activate lai:

```powershell
.\.venv\Scripts\Activate.ps1
```

Kiem tra dung moi truong:

```powershell
python --version
where python
```

Duong dan Python nen nam trong thu muc `.venv` cua project.

## Cach chay

1. Mo game dua xe truoc.
2. Dam bao cua so game dang focus va nhan phim `W/A/S/D/Space`.
3. Chay controller:

```powershell
python main.py
```

4. Dua hai tay len truoc webcam.
5. Bam `q` trong cua so camera de thoat.

## Dieu khien

| Cu chi | Phim gia lap | Tac dung |
| --- | --- | --- |
| Hai tay o giua man hinh | `W` | Chay toi |
| Nghieng hai tay sang trai | `A` | Re trai |
| Nghieng hai tay sang phai | `D` | Re phai |
| Dua hai tay len cao | `Space` | Boost/Nitro |
| Dua hai tay xuong thap | `S` | Phanh/Drift |
| Dua hai tay xuong va nghieng trai/phai | `S` + `A/D` | Drift trai/phai |
| Bo tay ra khoi camera | Tha phim | Dung gui input |

## Cau truc file

- `main.py`: diem chay chinh cua project.
- `CarGameController.py`: controller chinh cho game dua xe.
- `SteeringWheelDisplay.py`: ve vo lang ao tren man hinh camera.
- `keyinput.py`: gui phim vao Windows bang `SendInput`.
- `pointerGameController.py`: demo dieu khien chuot bang ngon tay.
- `leftHolderMouseButton.py`: demo giu/tha chuot trai bang cu chi.
- `requirements.txt`: danh sach thu vien can cai.

## Luu y ve `main.py`

`main.py` dang chay theo thu tu:

```python
CarGame.game()
Spliter.game()
Pointer.game()
```

`CarGame.game()` la vong lap camera lien tuc, nen hai module sau chi chay sau khi ban thoat cua so `FAIC Game` bang phim `q`.

## Chinh kich thuoc camera

Trong `CarGameController.py`, tim:

```python
FRAME_W = 640
FRAME_H = 480
```

Tang giam hai gia tri nay de doi kich thuoc khung camera. Neu may bi lag khi nhan dien hai tay, nen de `640x480` hoac thap hon.

Trong `pointerGameController.py` va `leftHolderMouseButton.py`, tim:

```python
cam_w, cam_h = 560, 480
```

## Loi thuong gap

### No Python at `...\Python311\python.exe`

Nguyen nhan: `.venv` duoc tao tu Python cu da bi xoa hoac copy tu may/user khac.

Cach sua:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### `AttributeError: module 'mediapipe' has no attribute 'solutions'`

Nguyen nhan: ban dang dung MediaPipe/Python qua moi so voi code hien tai.

Cach sua khuyen dung:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Neu van gap loi, cai ban MediaPipe cu hon:

```powershell
pip install "mediapipe==0.10.14" "numpy<2"
```

### Nhan dien du hai tay thi bi lag

- Giam kich thuoc camera ve `640x480`.
- Dam bao chi co mot ung dung dang dung webcam.
- Dong cac app nang khi demo.
- Tang anh sang phong de MediaPipe nhan tay on dinh hon.

## Ghi chu demo

- Nen dat camera ngang tam nguc hoac ngang mat.
- Nen dung phong co anh sang tot.
- Nen tranh co nhieu nguoi/tay xuat hien trong khung hinh.
- Neu game khong nhan phim, click lai vao cua so game de focus.
