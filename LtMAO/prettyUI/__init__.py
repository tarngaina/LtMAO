import threading
import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as tkfd
from LtMAO import pyRitoFile
from LtMAO import keeper
from memory_profiler import profile

TRANSPARENT = 'transparent'
ctk.set_appearance_mode('system')
tk_widgets = keeper.Keeper()


def create_main_app():
    # create main app
    tk_widgets.main_tk = ctk.CTk()
    tk_widgets.main_tk.geometry('1000x600')
    tk_widgets.main_tk.title('LtMAO')
    tk_widgets.main_tk.rowconfigure(0, weight=1)
    tk_widgets.main_tk.columnconfigure(0, weight=1)
    tk_widgets.main_tk.columnconfigure(1, weight=9)


def create_mainleft_frame():
    # create main left frame
    tk_widgets.mainleft_frame = ctk.CTkFrame(
        master=tk_widgets.main_tk
    )
    tk_widgets.mainleft_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)


def create_mainright_frame():
    # create main right frame
    tk_widgets.mainright_frame = ctk.CTkFrame(
        master=tk_widgets.main_tk
    )
    tk_widgets.mainright_frame.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)


def create_left_controls():
    # create left controls
    tk_widgets.mainleft_frame.columnconfigure(0, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(0, weight=1)

    # animaskviewer button
    tk_widgets.animaskviewer_button = ctk.CTkButton(
        master=tk_widgets.mainleft_frame,
        text='Animation Mask Viewer'
    )
    tk_widgets.animaskviewer_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.EW)
    tk_widgets.animaskviewer = keeper.Keeper()
    tk_widgets.animaskviewer.table_loaded = False


def create_right_pages(selected_page=0):
    if selected_page == 0:
        # animaskviewer page
        tk_widgets.mainright_frame.rowconfigure(0, weight=1)
        tk_widgets.mainright_frame.rowconfigure(1, weight=1)
        tk_widgets.mainright_frame.rowconfigure(2, weight=69)
        tk_widgets.mainright_frame.columnconfigure(0, weight=1)

        def create_inputs():
            # create input frame
            tk_widgets.animaskviewer.input_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.animaskviewer.input_frame.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.animaskviewer.input_frame.columnconfigure(0, weight=1)
            tk_widgets.animaskviewer.input_frame.columnconfigure(1, weight=8)
            tk_widgets.animaskviewer.input_frame.columnconfigure(2, weight=1)

            # create skl label
            tk_widgets.animaskviewer.skl_label = ctk.CTkLabel(
                master=tk_widgets.animaskviewer.input_frame,
                text='Input SKL',
                anchor=tk.W
            )
            tk_widgets.animaskviewer.skl_label.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            # create skl entry
            tk_widgets.animaskviewer.skl_entry = ctk.CTkEntry(
                master=tk_widgets.animaskviewer.input_frame,
            )
            tk_widgets.animaskviewer.skl_entry.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
            # create skl browse button

            def sklbrowse_cmd():
                skl_path = tkfd.askopenfilename(
                    title='Select SKL file',
                    filetypes=(
                        ('SKL files', '*.skl'),
                        ('All files', '*.*')
                    )
                )
                tk_widgets.animaskviewer.skl_entry.delete(0, tk.END)
                tk_widgets.animaskviewer.skl_entry.insert(tk.END, skl_path)
            tk_widgets.animaskviewer.sklbrowse_button = ctk.CTkButton(
                master=tk_widgets.animaskviewer.input_frame,
                text='Browse',
                anchor=tk.CENTER,
                command=sklbrowse_cmd
            )
            tk_widgets.animaskviewer.sklbrowse_button.grid(
                row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

            # create bin label
            tk_widgets.animaskviewer.bin_label = ctk.CTkLabel(
                master=tk_widgets.animaskviewer.input_frame,
                text='Input Animation BIN',
                anchor=tk.W
            )
            tk_widgets.animaskviewer.bin_label.grid(
                row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
            # create bin entry
            tk_widgets.animaskviewer.bin_entry = ctk.CTkEntry(
                master=tk_widgets.animaskviewer.input_frame,
            )
            tk_widgets.animaskviewer.bin_entry.grid(
                row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

            def binbrowse_cmd():
                bin_path = tkfd.askopenfilename(
                    title='Select Animation BIN file',
                    filetypes=(
                        ('BIN files', ['*.bin', '*.py']),
                        ('All files', '*.*')
                    )
                )
                tk_widgets.animaskviewer.bin_entry.delete(0, tk.END)
                tk_widgets.animaskviewer.bin_entry.insert(tk.END, bin_path)
            # create bin browse button
            tk_widgets.animaskviewer.binbrowse_button = ctk.CTkButton(
                master=tk_widgets.animaskviewer.input_frame,
                text='Browse',
                anchor=tk.CENTER,
                command=binbrowse_cmd
            )
            tk_widgets.animaskviewer.binbrowse_button.grid(
                row=1, column=2, padx=5, pady=5, sticky=tk.NSEW)

        def create_actions():
            # create action frame
            tk_widgets.animaskviewer.action_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame, fg_color=TRANSPARENT)
            tk_widgets.animaskviewer.action_frame.grid(
                row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.animaskviewer.action_frame.columnconfigure(0, weight=1)
            tk_widgets.animaskviewer.action_frame.columnconfigure(1, weight=1)
            tk_widgets.animaskviewer.action_frame.columnconfigure(2, weight=1)
            tk_widgets.animaskviewer.action_frame.columnconfigure(3, weight=69)

            # create load button
            def load_cmd():
                joint_names = []
                mask_names = []
                weights = []
                # read skl
                skl_path = tk_widgets.animaskviewer.skl_entry.get()
                if skl_path != '':
                    skl_file = pyRitoFile.SKL()
                    skl_file.read(skl_path)
                    joint_names = [joint.name for joint in skl_file.joints]
                # read bin
                bin_path = tk_widgets.animaskviewer.bin_entry.get()
                if bin_path != '':
                    bin_file = pyRitoFile.BIN()
                    bin_file.get_mask(bin_path)
                    mask_names = [mask for mask, weights in bin_file.masks]
                    weights = [weights for mask,
                               weights in bin_file.masks]

                # get table row and column length
                tk_widgets.animaskviewer.table_row = len(joint_names)
                tk_widgets.animaskviewer.table_column = len(mask_names)
                if tk_widgets.animaskviewer.table_row == 0 and tk_widgets.animaskviewer.table_column == 0:
                    return
                # create/load table frame
                if not tk_widgets.animaskviewer.table_loaded:
                    # horizontal scroll table frame
                    tk_widgets.animaskviewer.htable_frame = ctk.CTkScrollableFrame(
                        tk_widgets.mainright_frame,
                        fg_color=TRANSPARENT,
                        orientation=ctk.HORIZONTAL
                    )
                    tk_widgets.animaskviewer.htable_frame.grid(row=2, column=0, padx=5,
                                                               pady=5, sticky=tk.NSEW)
                    tk_widgets.animaskviewer.htable_frame.rowconfigure(
                        0, weight=1)
                    tk_widgets.animaskviewer.htable_frame.columnconfigure(
                        0, weight=1)

                    # vertical scroll table frame
                    tk_widgets.animaskviewer.vtable_frame = ctk.CTkScrollableFrame(
                        tk_widgets.animaskviewer.htable_frame,
                        fg_color=TRANSPARENT,
                        orientation=ctk.VERTICAL
                    )
                    tk_widgets.animaskviewer.vtable_frame.grid(
                        row=0, column=0, sticky=tk.NSEW)
                    tk_widgets.animaskviewer.vtable_frame.rowconfigure(
                        0, weight=1)
                    tk_widgets.animaskviewer.vtable_frame.columnconfigure(
                        0, weight=1)
                else:
                    # destroy loaded table
                    for widget in tk_widgets.animaskviewer.table_widgets:
                        if widget != None:
                            widget.destroy()

                # init empty table widgets
                tk_widgets.animaskviewer.table_widgets = [
                    None]*((tk_widgets.animaskviewer.table_row+1)*(tk_widgets.animaskviewer.table_column+1))

                # validate input as weight: x in [0.0, 1.0] cmd
                def validate_weight_cmd(x):
                    num_count = 0
                    not01_count = 0
                    sep_count = 0
                    for c in x:
                        if c in '01':
                            num_count += 1
                        elif c in '23456789':
                            num_count += 1
                            not01_count += 1
                        elif c == '.':
                            sep_count += 1
                        else:
                            return False
                    if num_count > 4:
                        return False
                    if sep_count > 1:
                        return False
                    if num_count > 0 and x[0] in '23456789':
                        return False
                    if num_count > 1 and x[0] == '1':
                        if not01_count > 0:
                            return False
                    return True

                for j in range(tk_widgets.animaskviewer.table_column+1):
                    for i in range(tk_widgets.animaskviewer.table_row+1):
                        windex = i*(tk_widgets.animaskviewer.table_column+1)+j
                        if windex == 0:
                            continue

                        # create mask name labels
                        if i == 0:
                            tk_widgets.animaskviewer.table_widgets[windex] = ctk.CTkLabel(
                                tk_widgets.animaskviewer.vtable_frame,
                                width=90,
                                text=mask_names[j-1]
                            )
                        # create joint name labels
                        elif j == 0:
                            tk_widgets.animaskviewer.table_widgets[windex] = ctk.CTkLabel(
                                tk_widgets.animaskviewer.vtable_frame,
                                width=160,
                                text=joint_names[i-1],
                                anchor=tk.W
                            )
                        # create weight entries
                        else:
                            tk_widgets.animaskviewer.table_widgets[windex] = ctk.CTkEntry(
                                tk_widgets.animaskviewer.vtable_frame,
                                width=80,
                                justify=tk.RIGHT,
                                validate='all',
                                validatecommand=(
                                    (tk_widgets.mainright_frame.register(
                                        validate_weight_cmd)),
                                    '%P'
                                )
                            )
                            # safe weight value if joints number > masks number
                            weight_value = '0'
                            try:
                                weight_value = weights[j-1][i-1]
                            except:
                                pass
                            tk_widgets.animaskviewer.table_widgets[windex].insert(
                                tk.END, weight_value)
                        tk_widgets.animaskviewer.table_widgets[windex].grid(
                            row=i, column=j, padx=5, pady=5, sticky=tk.NSEW)

                # update width of vertical scroll table frame (must)
                tk_widgets.animaskviewer.vtable_frame.configure(
                    width=170+(tk_widgets.animaskviewer.table_column+1)*100
                )
                tk_widgets.animaskviewer.vtable_frame.update_idletasks()
                # mark as table loaded
                tk_widgets.animaskviewer.table_loaded = True
            tk_widgets.animaskviewer.load_button = ctk.CTkButton(
                master=tk_widgets.animaskviewer.action_frame,
                text='Load',
                command=load_cmd
            )
            tk_widgets.animaskviewer.load_button.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

            # create save button
            def save_cmd():
                if not tk_widgets.animaskviewer.table_loaded:
                    return

                # init bin
                bin_file = pyRitoFile.BIN()
                # dump [(mask, weights),...]
                # start from column 1 because column 0 is just joint names
                for j in range(1, tk_widgets.animaskviewer.table_column+1):
                    mask_name = None
                    weights = []
                    for i in range(tk_widgets.animaskviewer.table_row+1):
                        windex = i*(tk_widgets.animaskviewer.table_column+1)+j
                        if windex == 0:
                            continue

                        # first row = mask names
                        if i == 0:
                            mask_name = tk_widgets.animaskviewer.table_widgets[windex].cget(
                                'text')
                        else:
                            weight = tk_widgets.animaskviewer.table_widgets[windex].get(
                            )
                            weights.append(weight)

                    bin_file.masks.append((mask_name, weights))

                # save to txt file (bin later)
                bin_path = tkfd.asksaveasfilename(
                    title='Select output TXT path',
                    filetypes=(
                        ('TXT files', '*.txt'),
                        ('All files', '*.*')
                    ),
                    defaultextension='.txt'
                )
                if bin_path != '':
                    bin_file.save_mask(bin_path)
            tk_widgets.animaskviewer.save_button = ctk.CTkButton(
                master=tk_widgets.animaskviewer.action_frame,
                text='Save',
                command=save_cmd
            )
            tk_widgets.animaskviewer.save_button.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

            # create clear button
            def clear_cmd():
                if not tk_widgets.animaskviewer.table_loaded:
                    return
                # destroy tk widgets
                for widget in tk_widgets.animaskviewer.table_widgets:
                    if widget != None:
                        widget.destroy()
                tk_widgets.animaskviewer.vtable_frame.destroy()
                tk_widgets.animaskviewer.htable_frame.destroy()
                tk_widgets.animaskviewer.table_loaded = False
                # del tk widgets from memory?
                # del tk_widgets.animaskviewer.table_widgets
                # del tk_widgets.animaskviewer.vtable_frame
                # del tk_widgets.animaskviewer.htable_frame
            tk_widgets.animaskviewer.clear_button = ctk.CTkButton(
                master=tk_widgets.animaskviewer.action_frame,
                text='Clear',
                command=clear_cmd
            )
            tk_widgets.animaskviewer.clear_button.grid(
                row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

        create_inputs()
        create_actions()


def start():
    # create UI
    create_main_app()
    create_mainleft_frame()
    create_mainright_frame()
    create_left_controls()
    create_right_pages()

    # loop the UI
    tk_widgets.main_tk.mainloop()
