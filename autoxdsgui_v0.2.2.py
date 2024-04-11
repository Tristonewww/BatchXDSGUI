import tkinter as tk
from tkinter import ttk, filedialog, font, messagebox
from tkinter import font as tkFont
from tkinter.font import Font 
import pandas as pd
import subprocess
import shutil
import os
import sys
import threading


# Define a new page class
class Page(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='white')

# Define the Input page
class XDSInput(tk.Frame):  # Assuming this inherits from tk.Frame
    def __init__(self, parent):
        super().__init__(parent, bg='white')

        # Instruction label
        instruction_frame = tk.Frame(self, bg='white')
        instruction_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10, columnspan=4)
        instruction_msg = "Please input all basic parameters used for XDS and then click 'Save and Run'. *Instamatic user only needs to input path."
        tk.Label(instruction_frame, text=instruction_msg, bg='white', wraplength=1000).pack(side="left")

        self.input_fields = {}

        # Row 1: Input path
        row1_frame = tk.Frame(self, bg='white')
        row1_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10) 
        tk.Label(row1_frame, text="1. Input path:", bg='white').grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.path_entry = tk.Entry(row1_frame)
        self.path_entry.grid(row=0, column=1, sticky="w", padx=(0, 30))  # Add padding between label and entry
        tk.Button(row1_frame, text="Browse", command=self.select_path).grid(row=0, column=2, sticky="w", padx=(5, 0))  # Add padding between entry and button

        # Row 2: NX, NY, QX, QY
        row2_frame = tk.Frame(self, bg='white')
        row2_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10, columnspan=4)
        labels_row2 = ["2. Detector parameters:     NX=", "NY=", "QX=", "QY="]
        for i, label in enumerate(labels_row2):
            tk.Label(row2_frame, text=label, bg='white').grid(row=0, column=i*2, sticky="w", padx=2)
            entry = tk.Entry(row2_frame, bg='white')
            entry.grid(row=0, column=i*2+1, sticky="w", padx=2)
            self.input_fields[label] = entry

        # Row 3: OVERLOAD
        row3_frame = tk.Frame(self, bg='white')
        row3_frame.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        tk.Label(row3_frame, text="3. Overloading:    OVERLOAD= ", bg='white').grid(row=0, column=0, sticky="w", padx=2)
        self.input_fields["OVERLOAD="] = tk.Entry(row3_frame, bg='white')
        self.input_fields["OVERLOAD="].grid(row=0, column=1, sticky="w", padx=2)

        # Row 4: INCLUDE_RESOLUTION_RANGE
        row4_frame = tk.Frame(self, bg='white')
        row4_frame.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        tk.Label(row4_frame, text="4. Rrsolution range:    INCLUDE_RESOLUTION_RANGE=    ", bg='white').grid(row=0, column=0, sticky="w", padx=2)
        self.input_fields["INCLUDE_RESOLUTION_RANGE="] = tk.Entry(row4_frame, bg='white')
        self.input_fields["INCLUDE_RESOLUTION_RANGE="].grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(row4_frame, text="    >>> Use space to interrupt", bg='white').grid(row=0, column=2, sticky="w", padx=2)
        
        # Row 5: ORGX, ORGY
        row5_frame = tk.Frame(self, bg='white')
        row5_frame.grid(row=5, column=0, sticky="w", padx=10, pady=10)
        tk.Label(row5_frame, text="5. Direct beam position:    ORGX=", bg='white').grid(row=0, column=0, sticky="w", padx=2)
        self.input_fields["ORGX="] = tk.Entry(row5_frame, bg='white')
        self.input_fields["ORGX="].grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(row5_frame, text="ORGY=", bg='white').grid(row=0, column=2, sticky="w", padx=2)
        self.input_fields["ORGY="] = tk.Entry(row5_frame, bg='white')
        self.input_fields["ORGY="].grid(row=0, column=3, sticky="w", padx=2)
        
        # Row 6: DETECTOR_DISTANCE
        row6_frame = tk.Frame(self, bg='white')
        row6_frame.grid(row=6, column=0, sticky="w", padx=10, pady=10)
        tk.Label(row6_frame, text="6. Cameralength:    DETECTOR_DISTANCE=", bg='white').grid(row=0, column=0, sticky="w", padx=2)
        self.input_fields["DETECTOR_DISTANCE="] = tk.Entry(row6_frame, bg='white')
        self.input_fields["DETECTOR_DISTANCE="].grid(row=0, column=1, sticky="w", padx=2)
        
        # Row 7: OSCILLATION_RANGE
        row7_frame = tk.Frame(self, bg='white')
        row7_frame.grid(row=7, column=0, sticky="w", padx=10, pady=10)
        tk.Label(row7_frame, text="7. Rotation step:    OSCILLATION_RANGE=", bg='white').grid(row=0, column=0, sticky="w", padx=2)
        self.input_fields["OSCILLATION_RANGE="] = tk.Entry(row7_frame, bg='white')
        self.input_fields["OSCILLATION_RANGE="].grid(row=0, column=1, sticky="w", padx=2)
        
        # Row 8: ROTATION_AXIS
        row8_frame = tk.Frame(self, bg='white')
        row8_frame.grid(row=8, column=0, sticky="w", padx=10, pady=10)
        tk.Label(row8_frame, text="8. Rotation axis:    ROTATION_AXIS=", bg='white').grid(row=0, column=0, sticky="w", padx=2)
        self.input_fields["ROTATION_AXIS="] = tk.Entry(row8_frame, bg='white')
        self.input_fields["ROTATION_AXIS="].grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(row8_frame, text="    >>> Use space to interrupt", bg='white').grid(row=0, column=2, sticky="w", padx=2)
        
        # Row 9: X-RAY_WAVELENGTH
        row9_frame = tk.Frame(self, bg='white')
        row9_frame.grid(row=9, column=0, sticky="w", padx=10, pady=10)
        tk.Label(row9_frame, text="9. Wavelength:    X-RAY_WAVELENGTH=", bg='white').grid(row=0, column=0, sticky="w", padx=2)
        self.input_fields["X-RAY_WAVELENGTH="] = tk.Entry(row9_frame, bg='white')
        self.input_fields["X-RAY_WAVELENGTH="].grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(row9_frame, text="    nm", bg='white').grid(row=0, column=2, sticky="w", padx=2)
        
        # Row 10: Beamstop Information and untrusted area
        row10_frame = tk.Frame(self, bg='white')
        row10_frame.grid(row=10, column=0, sticky="ew", padx=10, pady=10, columnspan=4)
        tk.Label(row10_frame, text="10. Advanced information (Please copy from XDS):    ", bg='white').pack(side="left")
        self.input_fields["Beamstop_Info"] = tk.Text(row10_frame, height=5, width=40, bg='white')
        self.input_fields["Beamstop_Info"].pack(side="left")              
        
        # Row 11: X-RAY_WAVELENGTH
        row9_frame = tk.Frame(self, bg='white')
        row9_frame.grid(row=11, column=0, sticky="w", padx=10, pady=10)
        tk.Label(row9_frame, text="11. Toggle if used:    Toggle_frame=", bg='white').grid(row=0, column=0, sticky="w", padx=2)
        self.input_fields["Toggle="] = tk.Entry(row9_frame, bg='white')
        self.input_fields["Toggle="].grid(row=0, column=1, sticky="w", padx=2)
        
        # Row 12: Save and Run button
        row11_frame = tk.Frame(self, bg='white')
        row11_frame.grid(row=12, column=0, sticky="w", padx=10, pady=10)
        tk.Button(row11_frame, text="Save and Run", command=self.save_and_run).pack(side="left")         

    def select_path(self):
        path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def save_and_run(self):
        # Collect all input values
        input_values = {}
        for label, field in self.input_fields.items():
            if isinstance(field, tk.Text):
                input_values[label] = field.get("1.0", "end-1c")  # For Text widgets
            else:
                input_values[label] = field.get()  # For Entry widgets
        input_path = self.path_entry.get()

        # Determine the directory to save the formatted parameters file
        output_file_path = os.path.join(input_path, "Input_parameters.txt") if input_path else "Input_parameters.txt"

        # Write input values to a file in the new format
        with open(output_file_path, "w") as file:
            file.write("###Uniform Experiment Settings###\n")
            file.write("###Example for FEI krios ###\n\n")

            # Writing reformatted parameters
            file.write(f"1. Pixel information for your camera:\n NX= {input_values.get('2. Detector parameters:     NX=')}   NY= {input_values.get('NY=')}  QX= {input_values.get('QX=')}  QY= {input_values.get('QY=')}  !Number and Size (mm) of pixel\n\n")
            file.write(f"2. Overload range for your camera:\n OVERLOAD= {input_values.get('OVERLOAD=')}          !default value dependent on the detector used\n\n")
            file.write(f"3. Resolution range for the 1st round:\n INCLUDE_RESOLUTION_RANGE=   {input_values.get('INCLUDE_RESOLUTION_RANGE=')}\n\n")
            file.write(f"4. Direct beam position\n ORGX= {input_values.get('ORGX=')}  ORGY=  {input_values.get('ORGY=')}\n\n")
            file.write(f"5. Cameralength\n DETECTOR_DISTANCE=  {input_values.get('DETECTOR_DISTANCE=')}\n\n")
            file.write(f"6. Oscillation range, degree per frame:\n OSCILLATION_RANGE={input_values.get('OSCILLATION_RANGE=')}\n\n")
            file.write(f"7. Rotation axis, depending on microscope:\n ROTATION_AXIS= {input_values.get('ROTATION_AXIS=')}  !cos(rotationaxis) cos(axis-90)  !in XDS.INP\n\n")
            file.write(f"8. Wavelength, nm (200kev 0.02508, 300kev 0.01968):\n X-RAY_WAVELENGTH=  {input_values.get('X-RAY_WAVELENGTH=')}     !used by IDXREF\n\n")

            # Writing beamstop information if present
            beamstop_info = input_values.get("Beamstop_Info")
            if beamstop_info.strip():
                file.write("###if you have a beam stop###\nBeamstop_start\n")
                file.write(beamstop_info)
                file.write("\nBeamstop_end\n###if you have a beam stop###\n")

            toggle_info = input_values.get("Toggle=")
            if toggle_info.strip():
                file.write("###if you use instamatic###\nToggle_on\n")
                file.write(toggle_info)
                file.write("\nToggle_off\n###if you use instamatic###\n") 
                
        main_app = self.master.master  
        main_app.set_input_path(input_path) 
        print(f"Parameters written to {output_file_path}")

# Define the XDSrunner page
class XDSrunner(Page):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='white')
        self.input_path = ""

        # Row 1: Description text
        description = tk.Label(self, text="Xdsrunner aims to do batch data processing based on the input parameters. Suggestion: Always do a demo data processing before batch", bg='white')
        description.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=5)

        # Row 2: Format transfer label
        tk.Label(self, text="1. Format transfer", bg='white').grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Row 3: Format transfer button and animation
        mrc_to_img_frame = tk.Frame(self, bg='white')
        mrc_to_img_frame.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        tk.Button(mrc_to_img_frame, text="mrc to img", command=self.run_mrc_to_img).pack(side="left", padx=25)
        self.animation_canvas = tk.Canvas(mrc_to_img_frame, width=150, height=20, bg='white', highlightthickness=0)
        self.animation_canvas.pack(side="left", padx=10)    
        self.mrc_to_img_animation_active = False
        self.mrc_to_img_animation_angle = 0

        # Row 4: XDSINP batch writing label
        tk.Label(self, text="2. xdsinp batch writing/Modify xdsinp generated by instamatic. Self beam center finding detects the strongest area in all .img", bg='white').grid(row=4, column=0, sticky="w", padx=10, pady=5)

        # Row 5: XDSINP batch writing buttons
        buttons_frame_row_5 = tk.Frame(self, bg='white')
        buttons_frame_row_5.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        tk.Button(buttons_frame_row_5, text="Generate xdsinp", command=self.run_xdswriter).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_5, text="Delete xds", command=self.confirm_delete_xds).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_5, text="Instamatic xdsinp", command=self.Instamatic_inpdelet).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_5, text="Self beam center finding", command=self.self_beam_center_nobeamstop).pack(side="left", padx=25)
        
        # Row 6: Run XDS in all folders label
        tk.Label(self, text="3. Run xds in all folders", bg='white').grid(row=6, column=0, sticky="w", padx=10, pady=5)

        # Row 7: Run XDS in all folders buttons and animation
        buttons_frame_row_7 = tk.Frame(self, bg='white')
        buttons_frame_row_7.grid(row=7, column=0, sticky="w", padx=10, pady=5)
        tk.Button(buttons_frame_row_7, text="xdsrunner", command=self.run_xdsrunner).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_7, text="Stop xdsrunner", command=self.stop_xdsrunner).pack(side="left", padx=25)
        self.xdsrunner_animation_canvas = tk.Canvas(buttons_frame_row_7, width=150, height=20, bg='white', highlightthickness=0)
        self.xdsrunner_animation_canvas.pack(side="left", padx=10)
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_angle = 0


        # Row 8: Show all information label
        tk.Label(self, text="4. Show all information", bg='white').grid(row=8, column=0, sticky="w", padx=10, pady=5)

        # Row 9: Show all information buttons
        buttons_frame_row_9 = tk.Frame(self, bg='white')
        buttons_frame_row_9.grid(row=9, column=0, sticky="w", padx=10, pady=5)
        tk.Button(buttons_frame_row_9, text="Show results", command=self.show_results).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_9, text="Update excel", command=self.update_excel).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_9, text="Open xdsrunner.xlsx", command=self.open_xdsrunner_excel).pack(side="left", padx=25)
        tk.Label(buttons_frame_row_9, text=">>> LibreOffice", bg='white').pack(side="left", padx=5)

        # Save processing
        self.processes = {}

    def run_mrc_to_img(self):
        script_path = os.path.join(os.path.dirname(__file__), "mrc2img.py")
        self.processes['mrc2img'] = subprocess.Popen(["python3", script_path, self.input_path])
        
        # Start Animation
        self.mrc_to_img_animation_active = True
        self.mrc_to_img_animation_angle = 0
        self.mrc_to_img_animate()
        
    def run_xdswriter(self):
        script_path = os.path.join(os.path.dirname(__file__), "xdswriter.py")
        self.processes['xdswriter'] = subprocess.Popen(["python3", script_path, self.input_path])

    def self_beam_center_nobeamstop(self):
        script_path = os.path.join(os.path.dirname(__file__), "self_beam_center_nobeamstop.py")
        self.processes['self_beam_center_nobeamstop'] = subprocess.Popen(["python3", script_path, self.input_path])

    def stop_xdswriter(self):
        if 'xdswriter' in self.processes:
            self.processes['xdswriter'].terminate()

    def run_xdsrunner(self):
        script_path = os.path.join(os.path.dirname(__file__), "xdsrunner.py")
        self.processes['xdsrunner'] = subprocess.Popen(["python3", script_path, self.input_path])

        # Start Animation
        self.xdsrunner_animation_active = True
        self.xdsrunner_animation_angle = 0
        self.xdsrunner_animate()

    def stop_xdsrunner(self):
        if 'xdsrunner' in self.processes:
            self.processes['xdsrunner'].terminate()
        
        # Stop Animation
        self.stop_xdsrunner_animation()

    def show_results(self):
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            self.display_excel_data(xdsrunner_excel_path)
        else:
            print("Cannot find xdsrunner.xlsx at the specified input path.")

    def update_excel(self):
        script_path = os.path.join(os.path.dirname(__file__), "xdsrecord1.py")
        self.processes['xdsrecord1'] = subprocess.Popen(["python3", script_path, self.input_path])

    def open_xdsrunner_excel(self):
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            try:
                subprocess.call(["libreoffice", "--calc", xdsrunner_excel_path])
            except Exception as e:
                print(f"Error opening file with LibreOffice Calc: {e}")
        else:
            print("Cannot find xdsrunner.xlsx at the specified input path.")

    def display_excel_data(self, file_path):
        df = pd.read_excel(file_path, engine='openpyxl')
    
        # Create Treeview widget and add a scrollbar
        tree = ttk.Treeview(self, show="headings")
        vsb = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree["columns"] = list(df.columns)
    
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'))
        
        # Design row colors
        tree.tag_configure('evenrow', background='lightgrey')
        tree.tag_configure('oddrow', background='white')
    
        # Set column headers and center-align the text
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
    
        # Add data to the Treeview with alternating colors
        for i, row in enumerate(df.itertuples(index=False, name=None)):
            tags = ('evenrow' if i % 2 == 0 else 'oddrow',)
            tree.insert("", "end", values=row, tags=tags)
    
        # Automatically adjust column widths based on content
        self.auto_adjust_columns(tree, df)
    
        # Place Treeview and scrollbar
        tree.grid(row=15, column=0, columnspan=3, sticky='nsew')
        vsb.grid(row=15, column=3, sticky='ns')
    
        # Configure grid layout for auto resizing
        self.grid_columnconfigure(0, weight=1)  # Make the Treeview column expandable
        self.grid_rowconfigure(15, weight=1)    # Make the Treeview row expandable


    def auto_adjust_columns(self, tree, df):
        for i, col in enumerate(tree["columns"]):
            max_width = 0
            for value in df[col]:
                width = font.Font().measure(str(value))
                if width > max_width:
                    max_width = width
            tree.column(col, width=max_width + 10)
            
    def confirm_delete_xds(self):
        #Display confirmation dialog for deleting xds files.
        response = messagebox.askyesno("Warning", "Warning! All xds files will be deleted. Are you sure?")
        if response:
            self.run_deletexds_script()

    def run_deletexds_script(self):
        #Run the deletexds.py script.
        script_path = os.path.join(os.path.dirname(__file__), "deletexds.py")
        subprocess.Popen(["python3", script_path, self.input_path])    

    def Instamatic_inpdelet(self):
        #Modify the xds.inp generated by @Instamatic
        script_path = os.path.join(os.path.dirname(__file__), "instamatic_inpdelete.py")
        subprocess.Popen(["python3", script_path, self.input_path])  

    def mrc_to_img_animate(self):
        if self.mrc_to_img_animation_active:
            self.animation_canvas.delete("all")

            # logic for anime
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1, start=self.mrc_to_img_animation_angle, extent=120, style=tk.ARC)
            self.animation_canvas.create_text(50, 10, text="Waiting... ", anchor="w")

            self.mrc_to_img_animation_angle = (self.mrc_to_img_animation_angle + 10) % 360

            # test .py processing 
            if self.processes['mrc2img'].poll() is None:
                self.after(100, self.mrc_to_img_animate)
            else:
                self.stop_mrc_to_img_animation()
    
    def stop_mrc_to_img_animation(self):
        self.mrc_to_img_animation_active = False
        self.animation_canvas.delete("all")   

    def xdsrunner_animate(self):
        if self.xdsrunner_animation_active:
            self.xdsrunner_animation_canvas.delete("all")

            # logic for anime
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.xdsrunner_animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1, start=self.xdsrunner_animation_angle, extent=120, style=tk.ARC)
            self.xdsrunner_animation_canvas.create_text(50, 10, text="Running... ", anchor="w")

            self.xdsrunner_animation_angle = (self.xdsrunner_animation_angle + 10) % 360

            # test .py processing 
            if self.processes['xdsrunner'].poll() is None:
                self.after(100, self.xdsrunner_animate)
            else:
                self.stop_xdsrunner_animation()
    
    def stop_xdsrunner_animation(self):
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_canvas.delete("all")

class UnitcellCorr(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.input_path = ""

        # Row 1: Instruction message
        instruction_msg = "Please input Space group and unit cell parameters."
        tk.Label(self, text=instruction_msg, bg='white').grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Row 2: Additional information
        additional_info = "Giving unit cell and space group keywords in all datasets is helpful for later data merging. XDS will refine unit cells individually."
        tk.Label(self, text=additional_info, bg='white').grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Row 3: Blind unit cell searching information
        blind_search_info = "Blind unit cell searching should be performed in XDSrunner. Check results in xdsrunner.xlsx"
        tk.Label(self, text=blind_search_info, bg='white').grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Row 4: Space group input
        space_group_frame = tk.Frame(self, bg='white')
        space_group_frame.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        tk.Label(space_group_frame, text="Space group:", bg='white').pack(side="left", padx=(0, 5))
        self.space_group_entry = tk.Entry(space_group_frame)
        self.space_group_entry.pack(side="left")

        # Row 5: Unit cell input
        unit_cell_frame = tk.Frame(self, bg='white')
        unit_cell_frame.grid(row=5, column=0, sticky="w", padx=22, pady=5)
        tk.Label(unit_cell_frame, text="Unit cell:", bg='white').pack(side="left", padx=(0, 5))
        self.unit_cell_entry = tk.Entry(unit_cell_frame)
        self.unit_cell_entry.pack(side="left")
        tk.Label(unit_cell_frame, text=">>>  Use space to interrupt", bg='white').pack(side="left", padx=(5, 0))

        # Row 6: Save button，
        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=6, column=0, sticky="w", padx=10, pady=5)
        tk.Button(buttons_frame, text="Save", command=self.save_cell_info).pack(side="left", padx=25)
        
        # Row 7: Update cell information button
        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=7, column=0, sticky="w", padx=10, pady=5)
        tk.Button(buttons_frame, text="Update cell information", command=self.update_cell_info).pack(side="left", padx=25)
        
        # Row 8: RUNxdsagain label
        runxdsagain_msg = "* Run XDS with updated .inp files."
        tk.Label(self, text=runxdsagain_msg, bg='white').grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Row 9: RUNxdsagain buttons
        buttons_frame_row_9 = tk.Frame(self, bg='white')
        buttons_frame_row_9.grid(row=9, column=0, sticky="w", padx=10, pady=5)
        tk.Button(buttons_frame_row_9, text="xdsrunner", command=self.run_xdsrunner2).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_9, text="Stop xdsrunner", command=self.stop_xdsrunner2).pack(side="left", padx=25)
        self.xdsrunner_animation_canvas = tk.Canvas(buttons_frame_row_9, width=150, height=20, bg='white', highlightthickness=0)
        self.xdsrunner_animation_canvas.pack(side="left", padx=10)
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_angle = 0
        
        # Row 10: Show all information label
        tk.Label(self, text="* Show all information", bg='white').grid(row=10, column=0, sticky="w", padx=10, pady=5)

        # Row 11: Show all information buttons
        buttons_frame_row_11 = tk.Frame(self, bg='white')
        buttons_frame_row_11.grid(row=11, column=0, sticky="w", padx=10, pady=5)
        tk.Button(buttons_frame_row_11, text="Show results", command=self.show_results).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_11, text="Update excel", command=self.update_excel).pack(side="left", padx=25)        
        tk.Button(buttons_frame_row_11, text="Open xdsrunner2.xlsx", command=self.open_xdsrunner_excel).pack(side="left", padx=25)
        tk.Label(buttons_frame_row_11, text=">>> LibreOffice", bg='white').pack(side="left", padx=5)

        # Save processing
        self.processes = {}

    def save_cell_info(self):
        space_group = self.space_group_entry.get()
        unit_cell = self.unit_cell_entry.get()
    
        # Get the input path from the main application
        main_app = self.master.master
        input_path = main_app.input_path
    
        if not input_path:
            print("Please select an input path first.")
            return  # Exit the method if no input path is set
    
        output_file_path = os.path.join(input_path, "Cell_information.txt")
    
        with open(output_file_path, "w") as file:
            file.write("#####Crystal Information#####\n\n")
            file.write(f"1.Space group\nSPACE_GROUP_NUMBER= {space_group}\n\n")
            file.write(f"2. Unit cell\nUNIT_CELL_CONSTANTS= {unit_cell}\n")
    
        print(f"Cell information saved to {output_file_path}")


    def update_cell_info(self):
        script_path = os.path.join(os.path.dirname(__file__), "cellcorr.py")
        self.processes['cellcorr'] = subprocess.Popen(["python3", script_path, self.input_path])

      
    def run_xdsrunner2(self):
        script_path = os.path.join(os.path.dirname(__file__), "xdsrunner2.py")
        self.processes['xdsrunner2'] = subprocess.Popen(["python3", script_path, self.input_path])
        
        # Start Animation
        self.xdsrunner_animation_active = True
        self.xdsrunner_animation_angle = 0
        self.xdsrunner_animate()

    def stop_xdsrunner2(self):
        if 'xdsrunner2' in self.processes:
            self.processes['xdsrunner2'].terminate()
            
        # Stop Animation
        self.stop_xdsrunner_animation()            

    def show_results(self):
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner2.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            self.display_excel_data(xdsrunner_excel_path)
        else:
            print("Cannot find xdsrunner2.xlsx at the specified input path.")

    def open_xdsrunner_excel(self):
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner2.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            try:
                subprocess.call(["libreoffice", "--calc", xdsrunner_excel_path])
            except Exception as e:
                print(f"Error opening file with LibreOffice Calc: {e}")
        else:
            print("Cannot find xdsrunner2.xlsx at the specified input path.")

    def update_excel(self):
        script_path = os.path.join(os.path.dirname(__file__), "xdsrecord.py")
        self.processes['xdsrecord'] = subprocess.Popen(["python3", script_path, self.input_path])

    def display_excel_data(self, file_path):
        df = pd.read_excel(file_path, engine='openpyxl')
    
        # Create Treeview widget and add a scrollbar
        tree = ttk.Treeview(self, show="headings")
        vsb = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree["columns"] = list(df.columns)
    
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'))
        
        # Design row colors
        tree.tag_configure('evenrow', background='lightgrey')
        tree.tag_configure('oddrow', background='white')
    
        # Set column headers and center-align the text
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
    
        # Add data to the Treeview with alternating colors
        for i, row in enumerate(df.itertuples(index=False, name=None)):
            tags = ('evenrow' if i % 2 == 0 else 'oddrow',)
            tree.insert("", "end", values=row, tags=tags)
    
        # Automatically adjust column widths based on content
        self.auto_adjust_columns(tree, df)
    
        # Place Treeview and scrollbar
        tree.grid(row=15, column=0, columnspan=3, sticky='nsew')
        vsb.grid(row=15, column=3, sticky='ns')
    
        # Configure grid layout for auto resizing
        self.grid_columnconfigure(0, weight=1)  # Make the Treeview column expandable
        self.grid_rowconfigure(15, weight=1)    # Make the Treeview row expandable
    
    
    def auto_adjust_columns(self, tree, df):
        for i, col in enumerate(tree["columns"]):
            max_width = 0
            for value in df[col]:
                width = font.Font().measure(str(value))
                if width > max_width:
                    max_width = width
            tree.column(col, width=max_width + 10)     

    def xdsrunner_animate(self):
        if self.xdsrunner_animation_active:
            self.xdsrunner_animation_canvas.delete("all")

            # logic for anime
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.xdsrunner_animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1, start=self.xdsrunner_animation_angle, extent=120, style=tk.ARC)
            self.xdsrunner_animation_canvas.create_text(50, 10, text="Running... ", anchor="w")

            self.xdsrunner_animation_angle = (self.xdsrunner_animation_angle + 10) % 360

            # test .py processing 
            if self.processes['xdsrunner2'].poll() is None:
                self.after(100, self.xdsrunner_animate)
            else:
                self.stop_xdsrunner_animation()
    
    def stop_xdsrunner_animation(self):
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_canvas.delete("all")            


class XDSpicker(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.input_path = ""

        # Row 1: Instruction
        note_label = tk.Label(self, text="Note: XDSpicker outputs xdspicker.xlsx. The excel table will be used for generating xscale.inp. Manual pick can always be performed by providing the xlsx file.", bg='white')
        note_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Row 2: Information for ISA filter
        isa_info_label = tk.Label(self, text="1. ISA_filter Model: Simple ISA filter ( >5 is suggested)", bg='white')
        isa_info_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Row 3: ISA Input
        isa_frame = tk.Frame(self, bg='white')
        isa_frame.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        isa_label = tk.Label(isa_frame, text="  Only use data with ISA > ", bg='white')
        isa_label.pack(side="left")  

        self.input_ISA = tk.Entry(isa_frame)
        self.input_ISA.pack(side="left") 
        
        # Row 4: Run ISA Filter Button
        isa_button = tk.Button(self, text="Run ISA filter", command=self.run_isa_filter)
        isa_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        # Row 5: Information for CC1/2 filter
        cc12_info_label = tk.Label(self, text="2. CC1/2_filter Model: Simple CC1/2 filter (Correct resolution first)", bg='white')
        cc12_info_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=5)        
        
        # Row 6: CC1/2 Input
        cc12_frame = tk.Frame(self, bg='white')
        cc12_frame.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        cc12_label = tk.Label(cc12_frame, text="  Only use data with CC1/2 > ", bg='white')
        cc12_label.pack(side="left")  

        self.input_cc12 = tk.Entry(cc12_frame)
        self.input_cc12.pack(side="left") 
        
        # Row 7: Run ISA Filter Button
        cc12_button = tk.Button(self, text="Run cc1/2 filter", command=self.run_cc12_filter)
        cc12_button.grid(row=6, column=0, padx=10, pady=5, sticky="w")        

        # Row 5: Future Features
        future_features_label = tk.Label(self, text="More filters will be added in the future... ...", bg='white')
        future_features_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    def run_isa_filter(self):
        xdspicker_filter_isa_value = self.input_ISA.get()
        script_path = os.path.join(os.path.dirname(__file__), "xdspicker_ISA_filter.py")
        subprocess.Popen(["python3", script_path, self.input_path, xdspicker_filter_isa_value])

    def run_cc12_filter(self):
        xdspicker_filter_cc12_value = self.input_cc12.get()
        script_path = os.path.join(os.path.dirname(__file__), "xdspicker_cc12_filter.py")
        subprocess.Popen(["python3", script_path, self.input_path, xdspicker_filter_cc12_value])        


class InpRefinement(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.input_path = ""

        # Row 1: Instruction1
        note_label = tk.Label(self, text="Note: Not mandatory step. Use models to refine all xds.inp in the target folder.", bg='white')
        note_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        # Row 2: Instruction2
        note_label = tk.Label(self, text="More models are under developing", bg='white')
        note_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

class Xscale(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.input_path = ""  # Initialize input_path attribute, to be set elsewhere

        # Row 1: Label for merging data instruction
        merge_data_label = tk.Label(self, text="Merge data from xdspicker.xlsx", bg='white')
        merge_data_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Row 2: Note about the usage of average unit cell parameters during merging
        note_label = tk.Label(self, text="Note: Average unit cell parameters will be used during merging/Make hkl and P4P for shelx", bg='white')
        note_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Row 3: Frame containing buttons for showing results and opening xscale.lp
        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        mergedata_button = tk.Button(buttons_frame, text="Merge Data", command=self.run_xdsmerge)
        mergedata_button.pack(side="left", padx=10)
        bus2shelx_button = tk.Button(buttons_frame, text="Bus to SHELX", command=self.run_xdsconv_shelx)
        bus2shelx_button.pack(side="left", padx=25)

        # Row 4: Label for merging data instruction
        merge_data_label = tk.Label(self, text="* Show all information", bg='white')
        merge_data_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Row 5: Frame containing buttons for showing results and opening xscale.lp
        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        # Inside Row 5: Button to show results
        show_result_button = tk.Button(buttons_frame, text="Show result", command=self.show_result)
        show_result_button.pack(side="left", padx=10)

        # Inside Row 5: Button to open xscale.lp file
        open_xscale_lp_button = tk.Button(buttons_frame, text="Open xscale.lp", command=self.open_xscale_lp)
        open_xscale_lp_button.pack(side="left", padx=25)

        # Row 6: Create an area to display the xscale.lp content
        self.result_text = tk.Text(self, wrap="word", height=15, font=("Times New Roman", 12))
        self.result_scrollbar = tk.Scrollbar(self, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=self.result_scrollbar.set)
        self.result_text.grid(row=6, column=0, sticky="nsew", padx=10, pady=5)
        self.result_scrollbar.grid(row=6, column=1, sticky="ns")

        # Configure grid layout for auto resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)        

    def run_xdsmerge(self):
        # Check if input_path is set before running the script
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        # Construct the path to the xdsmerge.py script and run it with the input path
        script_path = os.path.join(os.path.dirname(__file__), "xdsmerge.py")
        subprocess.Popen(["python3", script_path, self.input_path])

    def run_xdsconv_shelx(self):
        # Check if input_path is set before running the script
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        # Construct the path to the xdsmerge.py script and run it with the input path
        script_path = os.path.join(os.path.dirname(__file__), "xdsconv_shelx.py")
        subprocess.Popen(["python3", script_path, self.input_path])

    def show_result(self):
        # Check if the input_path is set
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        # Define the path to the merge directory inside the input path
        merge_dir_path = os.path.join(self.input_path, "merge")

        # Path to xscale.lp file
        xscale_lp_path = None
        for file in os.listdir(merge_dir_path):
            if file.lower() == 'xscale.lp':
                xscale_lp_path = os.path.join(merge_dir_path, file)
                break

        if not xscale_lp_path or not os.path.exists(xscale_lp_path):
            print("xscale.lp file not found in the merge directory.")
            return

        # Read the content of xscale.lp and extract the required part
        start_keyword = "SUBSET OF INTENSITY DATA"
        end_keyword = "STATISTICS OF INPUT DATA SET"
        content_to_display = ""
        capture = False

        with open(xscale_lp_path, "r") as file:
            for line in file:
                stripped_line = line.strip()  # Remove leading/trailing whitespace and special characters
                if start_keyword in stripped_line:
                    capture = True
                elif end_keyword in stripped_line:
                    break
                if capture:
                    content_to_display += line

        # Insert the extracted content into the Text widget
        self.result_text.delete("1.0", tk.END)  # Clear previous content
        self.result_text.insert("1.0", content_to_display)


    def open_xscale_lp(self):
        # Check if the input_path is set
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        # Define the path to the merge directory inside the input path
        merge_dir_path = os.path.join(self.input_path, "merge")

        # Path to xscale.lp file
        xscale_lp_path = None
        for file in os.listdir(merge_dir_path):
            if file.lower() == 'xscale.lp':
                xscale_lp_path = os.path.join(merge_dir_path, file)
                break

        if not xscale_lp_path or not os.path.exists(xscale_lp_path):
            print("xscale.lp file not found in the merge directory.")
            return

        # Create a Toplevel window to display the content
        result_window = tk.Toplevel(self)
        result_window.title("Xscale.lp Content")
        result_window.geometry("1200x600")  # Adjust the size as needed

        # Create a Text widget with a Scrollbar
        text_widget = tk.Text(result_window, wrap="word", font=("Times New Roman", 12))
        scrollbar = tk.Scrollbar(result_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Grid the Text widget and Scrollbar in the Toplevel window
        text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure grid layout for auto resizing
        result_window.grid_columnconfigure(0, weight=1)
        result_window.grid_rowconfigure(0, weight=1)

        # Read the content of xscale.lp and insert it into the Text widget
        with open(xscale_lp_path, "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)

class Clustering(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self.input_path = ""  # Initialize input_path attribute, to be set elsewhere

        # Row 1: Label for clustering
        merge_data_label = tk.Label(self, text="Clustering calculation based on Correlation Coefficients in Xscale.LP", bg='white')
        merge_data_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Row 2: Frame containing buttons for clustering
        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        mergedata_button = tk.Button(buttons_frame, text="Clustering", command=self.run_clustering)
        mergedata_button.pack(side="left", padx=2)

        # Row 3: Label for making clusters
        exclude_label = tk.Label(self, text="1. Exclude datasets for xscale ", bg='white')
        exclude_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Row 4: Frame containing inputs for excluding data      
        exclude_data_frame = tk.Frame(self, bg='white')
        exclude_data_frame.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        exclude_data_label = tk.Label(exclude_data_frame, text="Exclude datasets:   ", bg='white')
        exclude_data_label.pack(side="left")  
        self.input_exclude_data = tk.Entry(exclude_data_frame)
        self.input_exclude_data.pack(side="left") 
        info_label = tk.Label(exclude_data_frame, text="    >>> Use space to interrupt", bg='white')
        info_label.pack(side="left", padx=2)

        # Row 5: Button for excluding data
        exclude_data_button = tk.Button(self, text="Exclude data", command=self.exclude_data)
        exclude_data_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Row 6: Label for making clusters
        distance_label = tk.Label(self, text="2. Input distance to calculate clusters", bg='white')
        distance_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # Row 7: Frame containing inputs for clustering distance       
        cluster_distance_frame = tk.Frame(self, bg='white')
        cluster_distance_frame.grid(row=6, column=0, sticky="w", padx=10, pady=5)
        make_cluster_label = tk.Label(cluster_distance_frame, text="Distance used for dendrogram=   ", bg='white')
        make_cluster_label.pack(side="left")  
        self.input_cluster_distance = tk.Entry(cluster_distance_frame)
        self.input_cluster_distance.pack(side="left") 

        # Row 8: Button for making clusters
        cluster_distance_button = tk.Button(self, text="Make clusters", command=self.make_clusters)
        cluster_distance_button.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        
    def run_clustering(self):
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        script_path = os.path.join(os.path.dirname(__file__), "clustering.py")
        subprocess.Popen(["python3", script_path, self.input_path])
        
    def make_clusters(self):
        cluster_distance_value = self.input_cluster_distance.get()
        script_path = os.path.join(os.path.dirname(__file__), "make_clusters.py")
        subprocess.Popen(["python3", script_path, self.input_path, cluster_distance_value])

    def exclude_data(self):
        exclude_data = self.input_exclude_data.get()
        script_path = os.path.join(os.path.dirname(__file__), "exclude_data_clusters.py")
        subprocess.Popen(["python3", script_path, self.input_path, exclude_data])

class RedundencyAnalysis (Page):
    pass

class OnlineMicroED(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.input_path = ""  # Initialize input_path attribute
        
        # Initialize variables with "Waiting"
        self.online_current_space_group = "Waiting..."
        self.online_current_average_unit_cell = "Waiting..."
        self.current_round_completeness = "Waiting..."
        self.current_round_CChalf = "Waiting..."
        self.current_round_resolution = "Waiting..."

        self.online_last_space_group = "None"
        self.online_last_average_unit_cell = "None"
        self.last_round_completeness = "None"
        self.last_round_CChalf = "None"
        self.last_round_resolution = "None"

        # Row 1: Label for Online MicroED data processing
        merge_data_label = tk.Label(self, text="Online MicroED data processing, currently designed for Scilifelab", bg='white')
        merge_data_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Row 2: Note about saving input parameters and unit cell information
        note_label = tk.Label(self, text="Note: Please make sure input parameters and unit cell information have been saved.", bg='white')
        note_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Row 3: Additional note regarding navigation
        note_label = tk.Label(self, text="If not, please go to page XDSInput and UnitcellCorr first.", bg='white')
        note_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Row 4: Additional note regarding navigation
        note_label = tk.Label(self, text="One click to process all unprocessed data in the target folder. If you collect one wired dataset, delete it/remove it to Onlinemicroed folder and run Online MicroED again!", bg='white')
        note_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        # Row 5: Refresh button and animation
        refresh_frame = tk.Frame(self, bg='white')
        refresh_frame.grid(row=5, column=0, sticky="w", padx=110, pady=5)
        tk.Button(refresh_frame, text="Online MicroED", command=self.run_onlinemicroed).pack(side="left", padx=25)
        
        self.onlinemicroed_animation_canvas = tk.Canvas(refresh_frame, width=300, height=20, bg='white', highlightthickness=0)
        self.onlinemicroed_animation_canvas.pack(side="left", padx=10)
        self.onlinemicroed_animation_active = False
        self.onlinemicroed_animation_angle = 0

        # Row 6: Online processing result label
        result_label = tk.Label(self, text="*** Online processing result ***", bg='white')
        result_label.grid(row=6, column=0, sticky="w", padx=100, pady=5)

        # Row 7: Current Space Group
        space_group_frame = tk.Frame(self, bg='white')
        space_group_frame.grid(row=7, column=0, sticky="w", padx=46, pady=5)
        space_group_label = tk.Label(space_group_frame, text=" Current Space group  :", bg='white')
        space_group_label.pack(side="left")
        self.space_group_display = tk.Entry(space_group_frame, bg='lightgrey', width=10)
        self.space_group_display.pack(side="left", padx=(5, 0))
        self.space_group_display.insert(0, self.online_current_space_group)
        self.space_group_display.config(state='readonly')  # Set state to readonly after insertion

        last_space_group_text = "   last: " + str(self.online_last_space_group)
        self.last_space_group_label = tk.Label(space_group_frame, text=last_space_group_text, bg='white')
        self.last_space_group_label.pack(side="left")
        
        # Row 8: Current Average Unit Cell
        unit_cell_frame = tk.Frame(self, bg='white')
        unit_cell_frame.grid(row=8, column=0, sticky="w", padx=10, pady=5)
        unit_cell_label = tk.Label(unit_cell_frame, text=" Current average Unit cell  :", bg='white')
        unit_cell_label.pack(side="left")
        self.unit_cell_display = tk.Entry(unit_cell_frame, bg='lightgrey', width=50)
        self.unit_cell_display.pack(side="left", padx=(5, 0))
        self.unit_cell_display.insert(0, self.online_current_average_unit_cell)
        self.unit_cell_display.config(state='readonly')  # Set state to readonly after insertion    

        last_unit_cell_text = "   last: " + str(self.online_last_average_unit_cell)
        self.last_unit_cell_label = tk.Label(unit_cell_frame, text=last_unit_cell_text, bg='white')
        self.last_unit_cell_label.pack(side="left")    

        # Row 9: Current completeness
        current_round_completeness_frame = tk.Frame(self, bg='white')
        current_round_completeness_frame.grid(row=9, column=0, sticky="w", padx=46, pady=5)
        current_round_completeness_label = tk.Label(current_round_completeness_frame, text=" Current Completeness :", bg='white')
        current_round_completeness_label.pack(side="left")
        self.current_round_completeness_display = tk.Entry(current_round_completeness_frame, bg='lightgrey', width=10)
        self.current_round_completeness_display.pack(side="left", padx=(5, 0))
        self.current_round_completeness_display.insert(0, self.current_round_completeness)
        self.current_round_completeness_display.config(state='readonly')  # Set state to readonly after insertion

        last_round_completeness_text = "   last: " + str(self.last_round_completeness)
        self.last_round_completeness_label = tk.Label(current_round_completeness_frame, text=last_round_completeness_text, bg='white')
        self.last_round_completeness_label.pack(side="left")    

        # Row 10: Current cchalf
        current_round_CChalf_frame = tk.Frame(self, bg='white')
        current_round_CChalf_frame.grid(row=10, column=0, sticky="w", padx=46, pady=5)
        current_round_CChalf_label = tk.Label(current_round_CChalf_frame, text=" Current CChalf       :", bg='white')
        current_round_CChalf_label.pack(side="left")
        self.current_round_CChalf_display = tk.Entry(current_round_CChalf_frame, bg='lightgrey', width=10)
        self.current_round_CChalf_display.pack(side="left", padx=(5, 0))
        self.current_round_CChalf_display.insert(0, self.current_round_CChalf)
        self.current_round_CChalf_display.config(state='readonly')  # Set state to readonly after insertion

        last_round_CChalf_text = "   last: " + str(self.last_round_CChalf)
        self.last_round_CChalf_label = tk.Label(current_round_CChalf_frame, text=last_round_CChalf_text, bg='white')
        self.last_round_CChalf_label.pack(side="left") 

        # Row 11: Current Resolution
        current_round_resolution_frame = tk.Frame(self, bg='white')
        current_round_resolution_frame.grid(row=11, column=0, sticky="w", padx=46, pady=5)
        current_round_resolution_label = tk.Label(current_round_resolution_frame, text=" Current Resolution   :", bg='white')
        current_round_resolution_label.pack(side="left")
        self.current_round_resolution_display = tk.Entry(current_round_resolution_frame, bg='lightgrey', width=10)
        self.current_round_resolution_display.pack(side="left", padx=(5, 0))
        self.current_round_resolution_display.insert(0, self.current_round_resolution)
        self.current_round_resolution_display.config(state='readonly')  # Set state to readonly after insertion

        last_round_resolution_text = "   last: " + str(self.last_round_resolution)
        self.last_round_resolution_label = tk.Label(current_round_resolution_frame, text=last_round_resolution_text, bg='white')
        self.last_round_resolution_label.pack(side="left") 
        
        
        # Row 12: Open xscale.lp button
        buttons_frame_row_12 = tk.Frame(self, bg='white')
        buttons_frame_row_12.grid(row=12, column=0, sticky="w", padx=10, pady=5)
        tk.Button(buttons_frame_row_12, text="Check Current datasets", command=self.open_xdsrunner2).pack(side="left", padx=25)
        tk.Button(buttons_frame_row_12, text="Open Current xscale.lp", command=self.open_current_xscale_lp).pack(side="left", padx=25)


        # Row 13: Information
        note_label = tk.Label(self, text="* Check the result of round < ? >", bg='white')
        note_label.grid(row=13, column=0, sticky="w", padx=15, pady=5)        

                
        self.processes = {}

        self.refresh_count = 0  # Initialize refresh count

        
        
    def update_variable(self, variable_name, new_value):
        setattr(self, variable_name, new_value)
        entry_widget = getattr(self, variable_name + "_entry")
        entry_widget.config(state='normal')
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, new_value)
        entry_widget.config(state='readonly')

    def update_round_info(self):
        # Update last round information
        self.online_last_space_group = self.online_current_space_group
        self.online_last_average_unit_cell = self.online_current_average_unit_cell
        self.last_round_completeness = self.current_round_completeness
        self.last_round_CChalf = self.current_round_CChalf
        self.last_round_resolution = self.current_round_resolution

        # Update GUI for last round information
        self.update_label_text("last_space_group_label", "   last: " + str(self.online_last_space_group))
        self.update_label_text("last_unit_cell_label", "   last: " + str(self.online_last_average_unit_cell))
        self.update_label_text("last_round_completeness_label", "   last: " + str(self.last_round_completeness))
        self.update_label_text("last_round_CChalf_label", "   last: " + str(self.last_round_CChalf))
        self.update_label_text("last_round_resolution_label", "   last: " + str(self.last_round_resolution))

    def update_label_text(self, label_attribute, text):
        if hasattr(self, label_attribute):
            label = getattr(self, label_attribute)
            label.config(text=text)
        else:
            print(f"Attribute {label_attribute} not found in OnlineMicroED class")        
 
    def run_onlinemicroed(self):
        self.start_onlinemicroed_animation()
        # new thread
        processing_thread = threading.Thread(target=self.process_data)
        processing_thread.start()
        
    def process_data(self):   

        self.space_group_display.config(state='normal')
        self.space_group_display.delete(0, 'end')
        self.space_group_display.insert(0, "Waiting...")
        self.space_group_display.config(state='readonly')

        self.unit_cell_display.config(state='normal')
        self.unit_cell_display.delete(0, 'end')
        self.unit_cell_display.insert(0, "Waiting...")
        self.unit_cell_display.config(state='readonly') 

        self.current_round_completeness_display.config(state='normal')
        self.current_round_completeness_display.delete(0, 'end')
        self.current_round_completeness_display.insert(0, "Waiting...")
        self.current_round_completeness_display.config(state='readonly')

        self.current_round_CChalf_display.config(state='normal')
        self.current_round_CChalf_display.delete(0, 'end')
        self.current_round_CChalf_display.insert(0, "Waiting...")
        self.current_round_CChalf_display.config(state='readonly')
        
        self.current_round_resolution_display.config(state='normal')
        self.current_round_resolution_display.delete(0, 'end')
        self.current_round_resolution_display.insert(0, "Waiting...")
        self.current_round_resolution_display.config(state='readonly') 

        # Check if input_path is provide
        if not self.input_path:
            messagebox.showerror("Error", "No input path provided. Check the first page.")
            self.stop_onlinemicroed_animation()
            return  # Exit the function if no input path is provided        

        self.update_round_info()

        self.refresh_count += 1
        i = self.refresh_count  # Current round number

        # Step 1: Create folder
        online_microed_folder = os.path.join(self.input_path, 'onlinemicroed')
        os.makedirs(online_microed_folder, exist_ok=True)

        # Step 2: Check for necessary files and copy them to subfolders
        required_files = ['Input_parameters.txt', 'Cell_information.txt']
        for subdir in os.listdir(self.input_path):
            subdir_path = os.path.join(self.input_path, subdir)
            if os.path.isdir(subdir_path) and subdir != 'onlinemicroed':
                for file in required_files:
                    file_path = os.path.join(self.input_path, file)
                    if os.path.exists(file_path):
                        shutil.copy(file_path, subdir_path)
                    else:
                        messagebox.showerror("Error", f"Please provide {file} in the input path!")
                        self.stop_onlinemicroed_animation()
                        return
                
        # Step 3: Check for unprocessed data folders, excluding the 'onlinemicroed' folder
        unprocessed_folders = []  # List to hold paths of unprocessed folders
        for subdir in os.listdir(self.input_path):
            if subdir == 'onlinemicroed':
                continue  # Skip the 'onlinemicroed' folder
        
            subdir_path = os.path.join(self.input_path, subdir)
        
            # Confirm that subdir_path is a directory, not a file
            if not os.path.isdir(subdir_path):
                continue  # Skip if it's not a directory
        
            # Check if 'processed_tag.txt' exists in the directory
            processed_tag_path = os.path.join(subdir_path, 'processed_tag.txt')
            if os.path.exists(processed_tag_path):
                continue  # Skip this directory if the file exists
        
            # If 'processed_tag.txt' does not exist, add the directory to unprocessed_folders
            unprocessed_folders.append(subdir_path)
                                    
        
        # Step 4 & 5: Process each unprocessed data folder
        for folder in unprocessed_folders:
            self.process_folder(folder)

        # Step 6: Run xdsrecord.py
        script_path = os.path.dirname(__file__)
        subprocess.run(["python3", os.path.join(script_path, "xdsrecord.py"), self.input_path])

        # Step 7: Create round_i folder and copy xdsrunner2.xlsx
        round_folder = os.path.join(online_microed_folder, f"round_{i}")
        os.makedirs(round_folder, exist_ok=True)
        shutil.copy(os.path.join(self.input_path, 'xdsrunner2.xlsx'), os.path.join(round_folder, 'xdspicker.xlsx'))
        subprocess.run(["python3", os.path.join(script_path, "xdsmerge.py"), round_folder])
        
        
        # Step 8: Read from xscale.lp in the round_i folder
        merge_folder_path = os.path.join(round_folder, 'merge')
        if os.path.exists(merge_folder_path) and os.path.isdir(merge_folder_path):
            merge_folder_files = os.listdir(merge_folder_path)
            xscale_lp_file = next((file for file in merge_folder_files if file.lower() == 'xscale.lp'), None)
    
            if xscale_lp_file is None:
                print("xscale.lp file not found. Exiting...")
                self.stop_onlinemicroed_animation()
                return  

            # if exist, keep going
            xscale_lp_path = os.path.join(merge_folder_path, xscale_lp_file)
            with open(xscale_lp_path, 'r') as file:
                lines = file.readlines()

                    
            for line in lines:
                if "SPACE_GROUP_NUMBER=" in line:
                    self.online_current_space_group = line.split("=")[1].strip()
                    self.space_group_display.config(state='normal')
                    self.space_group_display.delete(0, 'end')
                    self.space_group_display.insert(0, self.online_current_space_group)
                    self.space_group_display.config(state='readonly')
    
                elif "UNIT_CELL_CONSTANTS=" in line:
                    self.online_current_average_unit_cell = line.split("=")[1].strip()
                    self.unit_cell_display.config(state='normal')
                    self.unit_cell_display.delete(0, 'end')
                    self.unit_cell_display.insert(0, self.online_current_average_unit_cell)
                    self.unit_cell_display.config(state='readonly')     

        # Step 9: Process xscale.lp file for additional data
        subset_of_intensity_found = False
        for line in lines:
            if "SUBSET OF INTENSITY" in line:
                subset_of_intensity_found = True
                continue
    
            if subset_of_intensity_found and "total" in line:
                values = line.split()
                self.current_round_completeness = values[4]
                self.current_round_completeness_display.config(state='normal')
                self.current_round_completeness_display.delete(0, 'end')
                self.current_round_completeness_display.insert(0, self.current_round_completeness)
                self.current_round_completeness_display.config(state='readonly')

                self.current_round_CChalf = values[10]  # 11th value including 'total'
                self.current_round_CChalf_display.config(state='normal')
                self.current_round_CChalf_display.delete(0, 'end')
                self.current_round_CChalf_display.insert(0, self.current_round_CChalf)
                self.current_round_CChalf_display.config(state='readonly')
                
                # Search backwards for a line with "*"
                for reverse_line in reversed(lines[:lines.index(line)]):
                    if "*" in reverse_line:
                        self.current_round_resolution = reverse_line.split()[0]
                        self.current_round_resolution_display.config(state='normal')
                        self.current_round_resolution_display.delete(0, 'end')
                        self.current_round_resolution_display.insert(0, self.current_round_resolution)
                        self.current_round_resolution_display.config(state='readonly') 
                        break
    
                break  # Exit loop after processing 'total' line
        # Print the updated values for verification
        print("< Round ", self.refresh_count, ">", "Total information")
        print("Current Round Completeness: ", self.current_round_completeness)
        print("Current Round CChalf: ", self.current_round_CChalf)
        print("Current Round Resolution: ", self.current_round_resolution)          
        print (f"********************************************************")        
        print (f"  Current round <", self.refresh_count, "> of online processing has been finished")
        print (f"********************************************************") 
        # Stop Animation
        self.stop_onlinemicroed_animation()
        
        
    def process_folder(self, folder):
        script_path = os.path.dirname(__file__)
        print(f"Processing folder: {folder}")
    
        mrc2img_path = os.path.join(script_path, "mrc2img.py")
        print(f"Running mrc2img.py on {folder}")
        subprocess.run(["python3", mrc2img_path, folder])    
    
        xdswriter_path = os.path.join(script_path, "xdswriter.py")
        print(f"Running xdswriter.py on {folder}")
        subprocess.run(["python3", xdswriter_path, folder])
    
        cellcorr_path = os.path.join(script_path, "cellcorr.py")
        print(f"Running cellcorr.py on {folder}")
        subprocess.run(["python3", cellcorr_path, folder])
    
        # Define the path for the new xds folder
        xds_folder = os.path.join(folder, "xds")
        if not os.path.exists(xds_folder):
            print(f"Expected xds folder not found: {xds_folder}")
            return
    
        print(f"Running XDS in {xds_folder}")
        subprocess.run("xds", cwd=xds_folder, shell=True)
        # Create a tag to identify processed folder
        processed_tag_path = os.path.join(folder, "processed_tag.txt")
        with open(processed_tag_path, 'w') as file:
            file.write(" ")
        print(f"{folder} has been processed")

    def open_current_xscale_lp(self):
        # Check if the input_path is set
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        i = self.refresh_count  # Current round number
        # Define the path to the merge directory inside the input path
        merge_dir_path = os.path.join(self.input_path, "onlinemicroed", f"round_{i}", "merge")

        # Path to xscale.lp file
        xscale_lp_path = None
        for file in os.listdir(merge_dir_path):
            if file.lower() == 'xscale.lp':
                xscale_lp_path = os.path.join(merge_dir_path, file)
                break

        if not xscale_lp_path or not os.path.exists(xscale_lp_path):
            print("xscale.lp file not found in the merge directory.")
            return
        
        # Create a Toplevel window to display the content
        result_window = tk.Toplevel(self)
        result_window.title("Xscale.lp Content")
        result_window.geometry("1200x600")  # Adjust the size as needed

        # Create a Text widget with a Scrollbar
        text_widget = tk.Text(result_window, wrap="word", font=("Times New Roman", 12))
        scrollbar = tk.Scrollbar(result_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Grid the Text widget and Scrollbar in the Toplevel window
        text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure grid layout for auto resizing
        result_window.grid_columnconfigure(0, weight=1)
        result_window.grid_rowconfigure(0, weight=1)

        # Read the content of xscale.lp and insert it into the Text widget
        with open(xscale_lp_path, "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)    

    def open_xdsrunner2(self):
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner2.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            try:
                subprocess.call(["libreoffice", "--calc", xdsrunner_excel_path])
            except Exception as e:
                print(f"Error opening file with LibreOffice Calc: {e}")
        else:
            print("Cannot find xdsrunner2.xlsx at the specified input path.")

    #Animation
    def start_onlinemicroed_animation(self):
        self.onlinemicroed_animation_active = True
        self.onlinemicroed_animation_angle = 0
        self.onlinemicroed_animate()
        
    def onlinemicroed_animate(self):
   
        if self.onlinemicroed_animation_active:
            self.onlinemicroed_animation_canvas.delete("all")

            # animate logic
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.onlinemicroed_animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1, start=self.onlinemicroed_animation_angle, extent=120, style=tk.ARC)
            self.onlinemicroed_animation_canvas.create_text(50, 10, text="Online data processing ...", anchor="w")

            self.onlinemicroed_animation_angle = (self.onlinemicroed_animation_angle + 10) % 360

            self.after(100, self.onlinemicroed_animate)
        else:
            self.stop_onlinemicroed_animation()

    def stop_onlinemicroed_animation(self):
        self.onlinemicroed_animation_active = False
        self.onlinemicroed_animation_canvas.delete("all")
         

        
# Main window class
class SmartLei(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("AutoxdsGUI")
        self.geometry("1200x620")

        # Create a ttk.Style object
        style = ttk.Style(self)
        style.theme_use('alt')

        # Create a Font object (e.g., 'Arial' font, size 12, bold)
        tab_font = Font(family="Arial", size=100, weight="bold")

        # Configure the style of TNotebook.Tab with the font object
        style.configure("TNotebook.Tab", font=tab_font, padding=[20, 5, 20, 5])

        # Create the notebook widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Initialize input_path
        self.input_path = None

        # Create pages and add them to the notebook
        self.pages = {}
        page_classes = [XDSInput, XDSrunner, UnitcellCorr, XDSpicker, InpRefinement, Xscale, Clustering, RedundencyAnalysis, OnlineMicroED]
        for F in page_classes:
            page = F(parent=self.notebook)
            self.pages[F.__name__] = page
            self.notebook.add(page, text=F.__name__)

        self.protocol("WM_DELETE_WINDOW", self.on_close)    
            

    def set_input_path(self, path):
        self.input_path = path  # refresh path
        for page_name, page in self.pages.items():
            if hasattr(page, 'input_path'):
                page.input_path = path
        self.update_title()

    def update_title(self):
        if self.input_path:
            self.title(f"AutoxdsGUI- {self.input_path}")
        else:
            self.title("AutoxdsGUI")

    def on_close(self):
        if messagebox.askyesno("Exit", "Are you sure you want to close the window? OnlineMicroED will disconnect."):
            self.destroy()           

if __name__ == "__main__":
    app = SmartLei()
    app.mainloop()

print ("Thank you for using!")
print ("Report bug: lei.wang@mmk.su.se")