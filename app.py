import flet as ft
import speech_recognition as sr
import threading

recognizer = sr.Recognizer()
stopper = None


def main(page: ft.Page):
    global stopper

    # --- PAGE STYLE ---
    page.title = "Speech to Text"
    page.bgcolor = "#0a0f1f"  # deep tech blue
    page.window_width = 500
    page.window_height = 600

    # --- GLASS EFFECT TEXTBOX ---
    output = ft.TextField(
    multiline=True,
    min_lines=6,
    max_lines=10,
    bgcolor="rgba(255,255,255,0.08)",  # glass panel
    color="black",                     # <-- TEXT IS NOW BLACK
    border_radius=12,
    border_color="rgba(0,150,255,0.4)",
    border_width=2,
    text_size=16,
    width=450,
    hint_text="Your transcribed text will appear here...",
    hint_style=ft.TextStyle(color="#6f7a8a")
)

    # --- STATUS TEXT ---
    status = ft.Text(
        "Press the mic to start",
        color="#7aa8ff",
        size=14,
        weight=ft.FontWeight.W_500
    )

    # --- CALLBACK ---
    def callback(recognizer, audio):
        try:
            text = recognizer.recognize_google(audio)
            output.value += text + " "
        except:
            pass

    # --- TOGGLE LISTENING ---
    def toggle_listening(e):
        global stopper

        if stopper is None:
            status.value = "Listening..."
            page.update()

            # Faster ambient noise adjustment
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)

            stopper = recognizer.listen_in_background(
                sr.Microphone(),
                callback,
                phrase_time_limit=4
            )
        else:
            stopper(wait_for_stop=False)
            stopper = None
            status.value = "Stopped"
            page.update()

    # --- NEON MIC BUTTON ---
    mic_button = ft.Container(
    content=ft.Text("🎤", size=60, color="#00c8ff"),
    width=140,
    height=140,
    bgcolor="#0d162b",
    border_radius=100,
    alignment=ft.alignment.Alignment(0, 0),
    on_click=toggle_listening,
    shadow=ft.BoxShadow(
        spread_radius=4,
        blur_radius=25,
        color="rgba(0,180,255,0.6)",
        offset=ft.Offset(0, 0)
    ),
    border=ft.Border.all(2, "#00aaff")   # <-- FIXED
)

    # --- LAYOUT ---
    page.add(
        ft.Column(
            [
                ft.Container(height=20),
                output,
                ft.Container(height=40),
                mic_button,
                ft.Container(height=20),
                status
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


# --- THIS MUST BE OUTSIDE THE FUNCTION ---
ft.run(main)