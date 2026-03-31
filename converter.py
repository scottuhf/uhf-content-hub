#!/usr/bin/env python3
"""
Upper Hand Fantasy — Video Converter
Converts exported graphics to DaVinci Resolve-compatible format.
Target: H.264 / High profile / yuv420p / faststart MP4

Requirements:
  - Python 3.8+  (python.org)
  - FFmpeg in PATH  (ffmpeg.org)

Run:  python converter.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import sys
import json
from pathlib import Path

# ── BRAND COLOURS ──────────────────────────────────────────────────────────────
BG        = "#061525"
BG_CARD   = "#0d1f33"
BG_DEEP   = "#030a12"
BORDER    = "#1a3a5c"
PINK      = "#ED0A73"
BLUE      = "#339AE9"
GREEN     = "#3ECF6A"
ORANGE    = "#FF6B35"
TEXT      = "#FFFFFF"
MUTED     = "#5a8ab0"
DIM       = "#2d4a63"

FONT_HEAD  = ("Helvetica", 11, "bold")
FONT_BODY  = ("Helvetica", 10)
FONT_SMALL = ("Helvetica", 9)
FONT_MONO  = ("Courier", 9)


# ── FFMPEG HELPERS ─────────────────────────────────────────────────────────────
def ffmpeg_available():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def ffprobe_codec(path):
    """Return (codec_name, profile) for the first video stream, or (None, None)."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_streams", str(path)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video":
                return stream.get("codec_name"), stream.get("profile")
    except Exception:
        pass
    return None, None


def build_output_path(input_path, suffix, output_dir):
    stem = Path(input_path).stem
    out_name = stem + suffix + ".mp4"
    if output_dir:
        return Path(output_dir) / out_name
    return Path(input_path).parent / out_name


def build_ffmpeg_cmd(input_path, output_path, fps, crf):
    return [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level:v", "4.2",
        "-pix_fmt", "yuv420p",
        "-crf", str(crf),
        "-r", str(fps),
        "-c:a", "aac",
        "-movflags", "+faststart",
        str(output_path),
    ]


# ── FILE ROW ───────────────────────────────────────────────────────────────────
class FileRow:
    def __init__(self, parent_frame, file_path, row_index, remove_cb):
        self.path       = Path(file_path)
        self.row_index  = row_index
        self.remove_cb  = remove_cb
        self.fps_var    = tk.StringVar(value="default")
        self.status     = "pending"   # pending | converting | done | error

        # Probe codec info in background
        self.codec, self.profile = None, None
        threading.Thread(target=self._probe, daemon=True).start()

        self._build(parent_frame)

    def _probe(self):
        self.codec, self.profile = ffprobe_codec(self.path)
        # Update label on main thread
        try:
            self.codec_label.after(0, self._update_codec_label)
        except Exception:
            pass

    def _update_codec_label(self):
        try:
            if self.codec == "vp9":
                text, color = "VP9 — Needs conversion", ORANGE
            elif self.codec == "h264" and self.profile and "High" not in self.profile:
                text, color = f"H.264 {self.profile} — Re-encode", ORANGE
            elif self.codec == "h264":
                text, color = "H.264 — Re-encoding to High", BLUE
            elif self.codec:
                text, color = f"{self.codec.upper()} — Converting", MUTED
            else:
                text, color = "Unknown format", DIM
            self.codec_label.config(text=text, fg=color)
        except Exception:
            pass

    def _build(self, parent):
        bg = BG_CARD if self.row_index % 2 == 0 else BG_DEEP

        self.frame = tk.Frame(parent, bg=bg, pady=0)
        self.frame.pack(fill=tk.X, padx=0, pady=1)

        # Left: accent bar
        tk.Frame(self.frame, bg=BORDER, width=3).pack(side=tk.LEFT, fill=tk.Y)

        inner = tk.Frame(self.frame, bg=bg, padx=12, pady=8)
        inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Row 1: filename + remove button
        row1 = tk.Frame(inner, bg=bg)
        row1.pack(fill=tk.X)

        name = self.path.name
        if len(name) > 58:
            name = name[:26] + "…" + name[-26:]
        tk.Label(row1, text=name, font=FONT_HEAD, bg=bg, fg=TEXT,
                 anchor="w").pack(side=tk.LEFT)

        self.status_dot = tk.Label(row1, text="●", font=FONT_SMALL,
                                   bg=bg, fg=DIM)
        self.status_dot.pack(side=tk.RIGHT, padx=(4, 0))

        tk.Button(row1, text="✕", font=FONT_SMALL, bg=bg, fg=DIM,
                  bd=0, relief="flat", activebackground=bg,
                  activeforeground=PINK, cursor="hand2",
                  command=lambda: self.remove_cb(self)).pack(
                      side=tk.RIGHT, padx=(8, 2))

        # Row 2: codec tag + size + fps override
        row2 = tk.Frame(inner, bg=bg)
        row2.pack(fill=tk.X, pady=(3, 0))

        self.codec_label = tk.Label(row2, text="Detecting…", font=FONT_SMALL,
                                    bg=bg, fg=MUTED)
        self.codec_label.pack(side=tk.LEFT)

        size_mb = self.path.stat().st_size / (1024 * 1024)
        size_str = f"{size_mb:.1f} MB" if size_mb >= 1 else f"{self.path.stat().st_size // 1024} KB"
        tk.Label(row2, text=f"  ·  {size_str}", font=FONT_SMALL,
                 bg=bg, fg=DIM).pack(side=tk.LEFT)

        # FPS override
        fps_frame = tk.Frame(row2, bg=bg)
        fps_frame.pack(side=tk.RIGHT)
        tk.Label(fps_frame, text="FPS:", font=FONT_SMALL, bg=bg,
                 fg=DIM).pack(side=tk.LEFT, padx=(0, 4))
        for val in ("30", "60", "default"):
            tk.Radiobutton(fps_frame, text=val, variable=self.fps_var, value=val,
                           font=FONT_SMALL, bg=bg, fg=MUTED,
                           activebackground=bg, selectcolor=bg,
                           indicatoron=True).pack(side=tk.LEFT, padx=2)

        # Progress bar (hidden until converting)
        self.progress_var = tk.DoubleVar(value=0)
        self.progress = ttk.Progressbar(inner, variable=self.progress_var,
                                        maximum=100, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(4, 0))
        self.progress.pack_forget()

        # Status message
        self.status_label = tk.Label(inner, text="", font=FONT_SMALL,
                                     bg=bg, fg=MUTED, anchor="w")
        self.status_label.pack(fill=tk.X)

    def set_status(self, status, msg=""):
        self.status = status
        colors = {
            "pending":    DIM,
            "converting": ORANGE,
            "done":       GREEN,
            "error":      PINK,
            "skipped":    MUTED,
        }
        dot_colors = {
            "pending":    DIM,
            "converting": ORANGE,
            "done":       GREEN,
            "error":      PINK,
            "skipped":    MUTED,
        }
        try:
            self.status_dot.config(fg=dot_colors.get(status, DIM))
            self.status_label.config(text=msg,
                                     fg=colors.get(status, MUTED))
            if status == "converting":
                self.progress.pack(fill=tk.X, pady=(4, 0))
                self.progress.start(15)
            else:
                self.progress.stop()
                self.progress.pack_forget()
        except Exception:
            pass


# ── MAIN APP ───────────────────────────────────────────────────────────────────
class ConverterApp:
    def __init__(self, root):
        self.root    = root
        self.rows    = []
        self.running = False

        root.title("Upper Hand Fantasy — Video Converter")
        root.configure(bg=BG)
        root.geometry("780x680")
        root.minsize(640, 520)
        root.resizable(True, True)

        # Try to set window icon (ignore if unavailable)
        try:
            root.iconbitmap(default="")
        except Exception:
            pass

        self._configure_styles()
        self._build_ui()
        self._check_ffmpeg()

    # ── STYLES ────────────────────────────────────────────────────────────────
    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar",
                         troughcolor=BG_DEEP,
                         background=BLUE,
                         bordercolor=BORDER,
                         lightcolor=BLUE,
                         darkcolor=BLUE)
        style.configure("TScrollbar",
                         troughcolor=BG_CARD,
                         background=BORDER,
                         bordercolor=BORDER)

    # ── UI BUILD ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Pink top border
        tk.Frame(self.root, bg=PINK, height=4).pack(fill=tk.X, side=tk.TOP)

        # ── Header
        header = tk.Frame(self.root, bg="#0a1929", pady=0)
        header.pack(fill=tk.X)

        h_inner = tk.Frame(header, bg="#0a1929", padx=24, pady=12)
        h_inner.pack(fill=tk.X)

        title_frame = tk.Frame(h_inner, bg="#0a1929")
        title_frame.pack(side=tk.LEFT)
        tk.Label(title_frame, text="UPPER HAND FANTASY", font=("Helvetica", 13, "bold"),
                 bg="#0a1929", fg=TEXT, letterSpacing=2).pack(anchor="w")
        tk.Label(title_frame, text="VIDEO CONVERTER", font=("Helvetica", 9),
                 bg="#0a1929", fg=MUTED).pack(anchor="w")

        tk.Label(h_inner, text="@upperhandfantasy", font=FONT_SMALL,
                 bg="#0a1929", fg=DIM).pack(side=tk.RIGHT)

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X)

        # ── Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Left panel
        left = tk.Frame(body, bg=BG, padx=20, pady=20)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right panel (settings)
        tk.Frame(body, bg=BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y)
        right = tk.Frame(body, bg=BG_CARD, padx=20, pady=20, width=220)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)

        self._build_left(left)
        self._build_right(right)

        # ── Bottom bar
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X)
        bottom = tk.Frame(self.root, bg="#0a1929", padx=20, pady=14)
        bottom.pack(fill=tk.X)
        self._build_bottom(bottom)

    def _build_left(self, parent):
        # Section label + Add button
        top = tk.Frame(parent, bg=BG)
        top.pack(fill=tk.X, pady=(0, 12))

        tk.Label(top, text="FILES", font=("Helvetica", 10, "bold"),
                 bg=BG, fg=MUTED, letterSpacing=3).pack(side=tk.LEFT)

        self.file_count_label = tk.Label(top, text="No files added",
                                         font=FONT_SMALL, bg=BG, fg=DIM)
        self.file_count_label.pack(side=tk.LEFT, padx=(12, 0))

        add_btn = tk.Button(top, text="+ Add Files", font=FONT_SMALL,
                            bg=BG_CARD, fg=BLUE, bd=0, relief="flat",
                            activebackground=BG_CARD, activeforeground=TEXT,
                            padx=12, pady=5, cursor="hand2",
                            command=self._browse_files)
        add_btn.pack(side=tk.RIGHT)

        # File list (scrollable)
        list_outer = tk.Frame(parent, bg=BORDER, bd=0)
        list_outer.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(list_outer, bg=BG_DEEP, bd=0,
                           highlightthickness=0, relief="flat")
        scrollbar = ttk.Scrollbar(list_outer, orient="vertical",
                                  command=canvas.yview)
        self.file_frame = tk.Frame(canvas, bg=BG_DEEP)

        self.file_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.file_frame, anchor="nw",
                              tags="inner")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Keep inner frame full width
        def _resize(e):
            canvas.itemconfig("inner", width=e.width)
        canvas.bind("<Configure>", _resize)

        # Mouse wheel
        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.canvas = canvas

        # Empty state label
        self.empty_label = tk.Label(
            self.file_frame,
            text="Click '+ Add Files' or drag files here",
            font=FONT_BODY, bg=BG_DEEP, fg=DIM, pady=40
        )
        self.empty_label.pack()

    def _build_right(self, parent):
        def section(text):
            tk.Label(parent, text=text, font=("Helvetica", 9, "bold"),
                     bg=BG_CARD, fg=MUTED).pack(anchor="w",
                                                  pady=(16, 6))
            tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X)

        tk.Label(parent, text="SETTINGS", font=("Helvetica", 10, "bold"),
                 bg=BG_CARD, fg=MUTED).pack(anchor="w", pady=(0, 16))

        # FPS
        section("DEFAULT FPS")
        self.fps_var = tk.StringVar(value="60")
        fps_frame = tk.Frame(parent, bg=BG_CARD)
        fps_frame.pack(fill=tk.X, pady=(8, 0))
        for fps in ("30", "60"):
            tk.Radiobutton(fps_frame, text=f"{fps} fps", variable=self.fps_var,
                           value=fps, font=FONT_BODY, bg=BG_CARD, fg=TEXT,
                           activebackground=BG_CARD, selectcolor=BG_CARD,
                           indicatoron=True).pack(side=tk.LEFT, padx=(0, 8))

        # CRF
        section("QUALITY (CRF)")
        crf_row = tk.Frame(parent, bg=BG_CARD)
        crf_row.pack(fill=tk.X, pady=(8, 0))
        self.crf_var = tk.StringVar(value="18")
        crf_entry = tk.Entry(crf_row, textvariable=self.crf_var, width=5,
                             font=("Helvetica", 13, "bold"), bg=BG_DEEP,
                             fg=TEXT, insertbackground=TEXT, bd=0,
                             relief="flat", justify="center")
        crf_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=4)
        tk.Label(crf_row, text="0 = lossless\n18 = recommended\n51 = smallest",
                 font=FONT_SMALL, bg=BG_CARD, fg=DIM, justify="left").pack(
                     side=tk.LEFT)

        # Output suffix
        section("OUTPUT SUFFIX")
        self.suffix_var = tk.StringVar(value="-davinci")
        tk.Entry(parent, textvariable=self.suffix_var, font=FONT_MONO,
                 bg=BG_DEEP, fg=BLUE, insertbackground=BLUE, bd=0,
                 relief="flat", ipady=6).pack(fill=tk.X, pady=(8, 0))
        tk.Label(parent, text="Added before .mp4", font=FONT_SMALL,
                 bg=BG_CARD, fg=DIM).pack(anchor="w", pady=(4, 0))

        # Output folder
        section("OUTPUT FOLDER")
        self.outdir_var = tk.StringVar(value="Same as input")
        tk.Label(parent, textvariable=self.outdir_var, font=FONT_SMALL,
                 bg=BG_CARD, fg=MUTED, wraplength=170, justify="left").pack(
                     anchor="w", pady=(8, 4))
        tk.Button(parent, text="Change Folder…", font=FONT_SMALL,
                  bg=BG_DEEP, fg=BLUE, bd=0, relief="flat",
                  activebackground=BG_DEEP, activeforeground=TEXT,
                  padx=10, pady=5, cursor="hand2",
                  command=self._choose_outdir).pack(anchor="w")
        tk.Button(parent, text="Reset to Same as Input", font=FONT_SMALL,
                  bg=BG_CARD, fg=DIM, bd=0, relief="flat",
                  activebackground=BG_CARD, activeforeground=TEXT,
                  padx=0, pady=2, cursor="hand2",
                  command=self._reset_outdir).pack(anchor="w", pady=(2, 0))

        self._outdir = None   # None = same as input

        # Required specs
        tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X, pady=(24, 8))
        tk.Label(parent, text="TARGET FORMAT", font=("Helvetica", 9, "bold"),
                 bg=BG_CARD, fg=DIM).pack(anchor="w")
        specs = [
            ("Codec",    "H.264",     GREEN),
            ("Profile",  "High",      GREEN),
            ("Level",    "4.2",       GREEN),
            ("Pixel",    "yuv420p",   GREEN),
            ("Audio",    "AAC",       GREEN),
            ("Flags",    "+faststart",GREEN),
        ]
        for key, val, col in specs:
            row = tk.Frame(parent, bg=BG_CARD)
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=key, font=FONT_SMALL, bg=BG_CARD,
                     fg=DIM, width=8, anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=val, font=FONT_MONO, bg=BG_CARD,
                     fg=col, anchor="w").pack(side=tk.LEFT)

    def _build_bottom(self, parent):
        self.convert_btn = tk.Button(
            parent, text="CONVERT ALL",
            font=("Helvetica", 12, "bold"),
            bg=PINK, fg=TEXT, bd=0, relief="flat",
            activebackground="#c40060", activeforeground=TEXT,
            padx=28, pady=10, cursor="hand2",
            command=self._start_conversion
        )
        self.convert_btn.pack(side=tk.LEFT)

        self.open_btn = tk.Button(
            parent, text="Open Output Folder",
            font=FONT_BODY,
            bg=BG_CARD, fg=BLUE, bd=0, relief="flat",
            activebackground=BG_CARD, activeforeground=TEXT,
            padx=16, pady=10, cursor="hand2",
            command=self._open_output_folder,
            state=tk.DISABLED
        )
        self.open_btn.pack(side=tk.LEFT, padx=(12, 0))

        self.clear_btn = tk.Button(
            parent, text="Clear All",
            font=FONT_BODY,
            bg=BG_CARD, fg=DIM, bd=0, relief="flat",
            activebackground=BG_CARD, activeforeground=PINK,
            padx=12, pady=10, cursor="hand2",
            command=self._clear_all
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(8, 0))

        self.bottom_status = tk.Label(
            parent, text="", font=FONT_SMALL,
            bg="#0a1929", fg=MUTED
        )
        self.bottom_status.pack(side=tk.RIGHT)

    # ── ACTIONS ───────────────────────────────────────────────────────────────
    def _browse_files(self):
        paths = filedialog.askopenfilenames(
            title="Select video files",
            filetypes=[
                ("Video files", "*.mp4 *.webm *.mov *.avi *.mkv *.m4v *.wmv"),
                ("All files", "*.*"),
            ]
        )
        for p in paths:
            if not any(r.path == Path(p) for r in self.rows):
                self._add_file(p)

    def _add_file(self, path):
        if self.empty_label.winfo_ismapped():
            self.empty_label.pack_forget()
        row = FileRow(self.file_frame, path, len(self.rows), self._remove_row)
        self.rows.append(row)
        self._update_count()

    def _remove_row(self, row):
        row.frame.destroy()
        self.rows.remove(row)
        if not self.rows:
            self.empty_label.pack()
        self._update_count()

    def _clear_all(self):
        for row in list(self.rows):
            row.frame.destroy()
        self.rows.clear()
        self.empty_label.pack()
        self._update_count()
        self.open_btn.config(state=tk.DISABLED)
        self.bottom_status.config(text="")

    def _choose_outdir(self):
        d = filedialog.askdirectory(title="Choose output folder")
        if d:
            self._outdir = d
            short = d if len(d) <= 28 else "…" + d[-26:]
            self.outdir_var.set(short)

    def _reset_outdir(self):
        self._outdir = None
        self.outdir_var.set("Same as input")

    def _update_count(self):
        n = len(self.rows)
        if n == 0:
            self.file_count_label.config(text="No files added", fg=DIM)
        else:
            self.file_count_label.config(
                text=f"{n} file{'s' if n != 1 else ''}", fg=MUTED)

    def _open_output_folder(self):
        folder = self._outdir
        if not folder and self.rows:
            folder = str(self.rows[0].path.parent)
        if folder and os.path.isdir(folder):
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.run(["open", folder])
            else:
                subprocess.run(["xdg-open", folder])

    # ── CONVERSION ────────────────────────────────────────────────────────────
    def _start_conversion(self):
        if self.running:
            return
        if not self.rows:
            messagebox.showinfo("No Files", "Add some video files first.")
            return

        try:
            crf = int(self.crf_var.get())
            assert 0 <= crf <= 51
        except (ValueError, AssertionError):
            messagebox.showerror("Invalid CRF",
                                 "CRF must be a number between 0 and 51.")
            return

        suffix = self.suffix_var.get().strip() or "-davinci"
        fps_default = int(self.fps_var.get())

        self.running = True
        self.convert_btn.config(state=tk.DISABLED, text="Converting…",
                                bg=BORDER)
        self.open_btn.config(state=tk.DISABLED)

        def run():
            total  = len(self.rows)
            done   = 0
            errors = 0
            last_outdir = None

            for row in self.rows:
                if row.status == "done":
                    done += 1
                    continue

                fps = fps_default
                if row.fps_var.get() != "default":
                    fps = int(row.fps_var.get())

                out_path = build_output_path(row.path, suffix, self._outdir)
                last_outdir = str(out_path.parent)
                cmd = build_ffmpeg_cmd(row.path, out_path, fps, crf)

                row.set_status("converting",
                               f"→ {out_path.name}")

                try:
                    proc = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True
                    )
                    if proc.returncode == 0:
                        size_mb = out_path.stat().st_size / (1024 * 1024)
                        row.set_status("done",
                                       f"✓ Saved: {out_path.name}  ({size_mb:.1f} MB)")
                        done += 1
                    else:
                        # Extract last error line from stderr
                        err_lines = [l.strip() for l in proc.stderr.splitlines() if l.strip()]
                        err_msg = err_lines[-1] if err_lines else "Unknown error"
                        row.set_status("error", f"✗ FFmpeg error: {err_msg}")
                        errors += 1
                except FileNotFoundError:
                    row.set_status("error", "✗ FFmpeg not found — is it installed?")
                    errors += 1
                except Exception as e:
                    row.set_status("error", f"✗ {e}")
                    errors += 1

                # Update bottom status
                self.root.after(0, lambda d=done, t=total, e=errors:
                    self.bottom_status.config(
                        text=f"{d}/{t} complete" + (f" · {e} error(s)" if e else ""),
                        fg=PINK if e else MUTED
                    )
                )

            self.root.after(0, lambda: self._on_conversion_done(done, errors, last_outdir))

        threading.Thread(target=run, daemon=True).start()

    def _on_conversion_done(self, done, errors, last_outdir):
        self.running = False
        self.convert_btn.config(state=tk.NORMAL, text="CONVERT ALL", bg=PINK)

        if last_outdir:
            self.open_btn.config(state=tk.NORMAL)

        if errors == 0:
            self.bottom_status.config(
                text=f"All {done} file(s) converted successfully ✓", fg=GREEN)
        else:
            self.bottom_status.config(
                text=f"{done} done · {errors} error(s)", fg=PINK)

    # ── FFMPEG CHECK ──────────────────────────────────────────────────────────
    def _check_ffmpeg(self):
        def check():
            if not ffmpeg_available():
                self.root.after(0, self._warn_no_ffmpeg)
        threading.Thread(target=check, daemon=True).start()

    def _warn_no_ffmpeg(self):
        msg = (
            "FFmpeg was not found in your PATH.\n\n"
            "To use this converter:\n"
            "1. Download FFmpeg from  ffmpeg.org/download.html\n"
            "2. Extract it and copy ffmpeg.exe to a folder\n"
            "3. Add that folder to your Windows PATH, OR\n"
            "   place ffmpeg.exe in the same folder as this script.\n\n"
            "Then restart the converter."
        )
        messagebox.showwarning("FFmpeg Not Found", msg)


# ── ENTRY POINT ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
