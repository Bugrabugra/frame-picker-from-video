import pathlib
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import PhotoImage
import cv2


# parametreleri ekle

class Window:
    def __init__(self):
        self.dictWidgetRows = {
            "frames_folder_location_button": 0,
            "frames_folder_location_label": 0,
            "frame_rate_label_first_part": 1,
            "frame_rate_input": 1,
            "frame_rate_label_last_part": 1,
            "video_button": 2,
            "video_folder_location_label": 2,
            "image": 3,
            "frame_name_label": 4,
            "navigation_buttons_frame": 5,
            "delete_frame_button": 6
        }
        self.label = None
        self.img = None
        self.images = None
        self.image_pos = 0
        self.video_folder_location = ""
        self.frames_folder_location = ""
        self.frame_rate = 1
        self.frame_name_label = None
        self.frame_rate_input = None
        self.root = tk.Tk()
        self.navigation_buttons_frame = tk.Frame(self.root)
        self.root.title("Frame Picker")
        self.frames_folder_location_button_packer()
        self.root.mainloop()

    def delete_frame(self):
        print()

    def open_confirm_delete_dialog(self):
        is_delete = mb.askyesno("Delete", "Are you sure you want to delete his frame?")
        if is_delete:
            self.delete_frame()

    def delete_frame_button_packer(self):
        delete_frame_button = tk.Button(
            self.root, text = "Delete frame", bg = "#FF6347", command = self.open_confirm_delete_dialog
        )
        delete_frame_button.grid(
            row = self.dictWidgetRows["delete_frame_button"], column = 0, columnspan = 2, padx = 16, pady = 6
        )

    def frame_rate_packer(self):
        frame_rate_label = tk.Label(self.root, text = "Extract images every")
        frame_rate_label.grid(
            row = self.dictWidgetRows["frame_rate_label_first_part"], column = 0, sticky = "W", padx = 16, pady = 6
        )

        frame_rate_values_frame = tk.Frame(self.root)
        frame_rate_values_frame.grid(row = self.dictWidgetRows["frame_rate_input"], column = 1, sticky = "W")

        self.frame_rate_input = tk.Entry(frame_rate_values_frame, width = 8)
        self.frame_rate_input.insert(0, "1")
        self.frame_rate_input.grid(
            row = self.dictWidgetRows["frame_rate_input"], column = 0, sticky = "W", padx = 4, pady = 6
        )

        seconds = tk.Label(frame_rate_values_frame, text = "second(s)")
        seconds.grid(
            row = self.dictWidgetRows["frame_rate_label_last_part"], column = 1, sticky = "W", padx = 4, pady = 6
        )

    def frame_name_label_packer(self):
        self.frame_name_label = tk.Label(self.root, text = "1.jpg")
        self.frame_name_label.grid(
            row = self.dictWidgetRows["frame_name_label"], column = 0, columnspan = 2, padx = 16, pady = 6
        )

    def navigation_buttons_frame_packer(self):
        self.navigation_buttons_frame.grid(
            row = self.dictWidgetRows["navigation_buttons_frame"], column = 0, columnspan = 2, padx = 16, pady = 6
        )
        self.previous_image_button_packer()
        self.next_image_button_packer()

    def previous_image_button_packer(self):
        previous_image_button = tk.Button(
            self.navigation_buttons_frame, text = "<<<", command = lambda: self.show_next_image(-1)
        )
        previous_image_button.grid(row = 0, column = 0, padx = 16, pady = 6)
        previous_image_button.grid_rowconfigure(0, weight = 1)

    def next_image_button_packer(self):
        next_image_button = tk.Button(
            self.navigation_buttons_frame, text = ">>>", command = lambda: self.show_next_image(1)
        )
        next_image_button.grid(row = 0, column = 1, padx = 16, pady = 6)

    def frames_folder_location_button_packer(self):
        frames_folder_location_button = tk.Button(
            self.root, text = "Choose folder to save frames", command = self.set_frames_folder_location
        )
        frames_folder_location_button.grid(
            row = self.dictWidgetRows["frames_folder_location_button"], column = 0, sticky = "W", padx = 16, pady = 6
        )

    def frames_folder_location_label_packer(self):
        frames_folder_location_label = tk.Label(
            self.root, text = self.frames_folder_location
        )
        frames_folder_location_label.grid(
            row = self.dictWidgetRows["frames_folder_location_label"], column = 1, sticky = "W", padx = 16, pady = 6
        )

    def video_folder_location_label_packer(self):
        video_folder_location_label = tk.Label(self.root, text = self.video_folder_location)
        video_folder_location_label.grid(
            row = self.dictWidgetRows["video_folder_location_label"], column = 1, sticky = "W", padx = 16, pady = 6
        )

    def set_frames_folder_location(self):
        frames_folder_location = fd.askdirectory()
        self.frames_folder_location = frames_folder_location

        if self.frames_folder_location:
            self.frames_folder_location_label_packer()
            self.frame_rate_packer()
            self.video_button_packer()

    def show_next_image(self, order):
        if order == 1:
            if self.image_pos < len(self.images) - 1:
                self.image_pos += order
            else:
                self.image_pos = 0
        else:
            if self.image_pos > 0:
                self.image_pos += order
            else:
                self.image_pos = 0

        self.frame_name_label["text"] = str(self.image_pos + 1) + ".png"
        self.img = PhotoImage(file = self.images[self.image_pos])
        self.label["image"] = self.img

    def video_button_packer(self):
        video_button = tk.Button(self.root, text = "Choose video file", command = self.open_video_file)
        video_button.grid(row = self.dictWidgetRows["video_button"], column = 0, sticky = "W", padx = 16, pady = 6)

    def label_image_packer(self):
        self.img = PhotoImage(file = self.images[self.image_pos])
        self.label = tk.Label(self.root, image = self.img)
        self.label.grid(row = self.dictWidgetRows["image"], column = 0, columnspan = 2, padx = 16, pady = 6)

    def get_frame(self, sec, video, count):
        video_capture = cv2.VideoCapture(video)
        video_capture.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        has_frames, image = video_capture.read()
        if has_frames:
            cv2.imwrite(self.frames_folder_location + "/" + str(count) + ".png", image)
        return has_frames

    def open_video_file(self):
        count = 1
        file_types = (('video files', '*.mp4'),)
        video_file = fd.askopenfile(filetypes = file_types)
        self.video_folder_location = video_file.name

        video = video_file.name

        sec = 0
        self.frame_rate = int(self.frame_rate_input.get())

        success = self.get_frame(sec, video, count)
        while success:
            count = count + 1
            sec = sec + self.frame_rate
            sec = round(sec, 2)
            success = self.get_frame(sec, video, count)

        self.images = list(sorted(pathlib.Path(self.frames_folder_location).glob("*.png")))
        self.video_folder_location_label_packer()
        self.label_image_packer()
        self.frame_name_label_packer()
        self.navigation_buttons_frame_packer()
        self.delete_frame_button_packer()


win = Window()
