
import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as tkfd

from LtMAO import pyRitoFile, cdtb_hashes, animask_viewer, leaguefile_inspector
from LtMAO.prettyUI.helper import Keeper, Log

import os
import os.path
from threading import Thread
from traceback import format_exception


def create_main_app_and_frames():
    # create main app
    tk_widgets.main_tk = ctk.CTk()
    tk_widgets.main_tk.geometry('1000x620')
    tk_widgets.main_tk.title('LtMAO')

    tk_widgets.main_tk.rowconfigure(0, weight=100)
    tk_widgets.main_tk.rowconfigure(1, weight=1)
    tk_widgets.main_tk.columnconfigure(0, weight=1)
    # create top frame
    tk_widgets.maintop_frame = ctk.CTkFrame(
        tk_widgets.main_tk,
        fg_color=TRANSPARENT
    )
    tk_widgets.maintop_frame.grid(
        row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    # create bottom frame
    tk_widgets.mainbottom_frame = ctk.CTkFrame(
        tk_widgets.main_tk,
        height=30
    )
    tk_widgets.mainbottom_frame.grid(
        row=1, column=0, padx=0, pady=2, sticky=tk.NSEW)

    tk_widgets.maintop_frame.rowconfigure(0, weight=1)
    tk_widgets.maintop_frame.columnconfigure(0, weight=0)
    tk_widgets.maintop_frame.columnconfigure(1, weight=1)
    # create top left frame
    tk_widgets.mainleft_frame = ctk.CTkFrame(
        tk_widgets.maintop_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.mainleft_frame.grid(
        row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    # create top right frame
    tk_widgets.mainright_frame = ctk.CTkFrame(
        tk_widgets.maintop_frame
    )
    tk_widgets.mainright_frame.grid(
        row=0, column=1, padx=0, pady=0, sticky=tk.NSEW)


def create_page_controls():
    # change top left & top right weight
    tk_widgets.mainright_frame.columnconfigure(0, weight=1)
    tk_widgets.mainright_frame.rowconfigure(0, weight=1)

    tk_widgets.mainleft_frame.columnconfigure(0, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(0, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(1, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(2, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(3, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(4, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(5, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(6, weight=699)

    # create left controls buttons
    def control_cmd(x):
        for id, control_button in enumerate(tk_widgets.control_buttons):
            if id == x:
                # highlight the active control
                control_button.configure(
                    fg_color=tk_widgets.active_control_fg_color)
            else:
                # empty background for other controls
                control_button.configure(fg_color=TRANSPARENT)
        # create page depend on control
        select_right_page(x)
    tk_widgets.select_control = control_cmd
    tk_widgets.control_buttons = [
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='cslmao',
            command=lambda: control_cmd(0)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='leaguefile_inspector',
            command=lambda: control_cmd(1)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='animask_viewer',
            command=lambda: control_cmd(2)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='vo_helper',
            command=lambda: control_cmd(3)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='Log',
            command=lambda: control_cmd(4)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='Setting',
            command=lambda: control_cmd(5)
        )
    ]
    for id, control_button in enumerate(tk_widgets.control_buttons):
        control_button.grid(
            row=id, column=0, padx=5, pady=5, sticky=tk.N+tk.EW)
    # get active color for active control
    tk_widgets.active_control_fg_color = tk_widgets.control_buttons[0].cget(
        'fg_color')

    # init pages data base on control buttons
    tk_widgets.pages = []
    for i in range(len(tk_widgets.control_buttons)):
        # each keeper for each page
        tk_widgets.pages.append(Keeper())
        # init page frame
        tk_widgets.pages[i].page_frame = None

    # reference page
    tk_widgets.LFI = tk_widgets.pages[1]
    tk_widgets.AMV = tk_widgets.pages[2]
    tk_widgets.LOG = tk_widgets.pages[4]

    # bonus init stuffs
    tk_widgets.LOG.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.LOG.page_frame.grid(
        row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    tk_widgets.LOG.page_frame.columnconfigure(0, weight=1)
    tk_widgets.LOG.page_frame.rowconfigure(0, weight=1)
    tk_widgets.LOG.log_textbox = ctk.CTkTextbox(
        tk_widgets.LOG.page_frame,
        corner_radius=0,
        wrap=tk.NONE,
        state=tk.DISABLED,
        border_spacing=10
    )
    tk_widgets.LOG.log_textbox.grid(row=0, column=0, sticky=tk.NSEW)
    Log.log_textbox = tk_widgets.LOG.log_textbox

    # select first page
    tk_widgets.select_control(0)


def select_right_page(selected):
    for page in tk_widgets.pages:
        if page.page_frame != None:
            page.page_frame.grid_forget()

    # create page depend on selected page
    if selected == 0:
        pass
    elif selected == 1:
        if tk_widgets.LFI.page_frame == None:
            tk_widgets.LFI.page_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame,
                fg_color=TRANSPARENT,
            )
            tk_widgets.LFI.page_frame.columnconfigure(0, weight=1)
            tk_widgets.LFI.page_frame.rowconfigure(0, weight=1)
            tk_widgets.LFI.page_frame.rowconfigure(1, weight=699)

            tk_widgets.LFI.loaded_list = []

            # create input frame
            tk_widgets.LFI.input_frame = ctk.CTkFrame(
                tk_widgets.LFI.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.LFI.input_frame.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.LFI.input_frame.rowconfigure(0, weight=1)
            tk_widgets.LFI.input_frame.columnconfigure(0, weight=1)
            tk_widgets.LFI.input_frame.columnconfigure(1, weight=1)
            tk_widgets.LFI.input_frame.columnconfigure(2, weight=1)
            tk_widgets.LFI.input_frame.columnconfigure(3, weight=699)

            # create view frame
            tk_widgets.LFI.view_frame = ctk.CTkScrollableFrame(
                tk_widgets.LFI.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.LFI.view_frame.grid(
                row=1, column=0, padx=0, pady=0, sticky=tk.NSEW)
            tk_widgets.LFI.view_frame.columnconfigure(0, weight=1)
            tk_widgets.LFI.view_frame.unbind_all('<MouseWheel>')

            # read one file function
            def read_file(file_path, hastables=None, ignore_error=False):
                path, size, json = leaguefile_inspector.try_read(
                    file_path, hastables, ignore_error)
                if ignore_error:
                    if size == None and json == None:
                        return

                # id of this file
                file_frame_id = len(tk_widgets.LFI.loaded_list)
                # create file frame
                file_frame = ctk.CTkFrame(
                    tk_widgets.LFI.view_frame
                )
                file_frame.grid(row=file_frame_id, column=0,
                                padx=2, pady=5, sticky=tk.NSEW)
                file_frame.columnconfigure(0, weight=1)
                file_frame.rowconfigure(0, weight=1)
                # create top file frame
                top_file_frame = ctk.CTkFrame(
                    file_frame
                )
                top_file_frame.grid(row=0, column=0,
                                    padx=0, pady=0, sticky=tk.NSEW)
                top_file_frame.columnconfigure(0, weight=0)
                top_file_frame.columnconfigure(1, weight=1)
                top_file_frame.columnconfigure(2, weight=0)
                top_file_frame.columnconfigure(3, weight=0)
                top_file_frame.rowconfigure(0, weight=1)
                # create file button

                def view_cmd(file_frame_id):
                    toggle = tk_widgets.LFI.loaded_list[file_frame_id][2]
                    text_frame = tk_widgets.LFI.loaded_list[file_frame_id][3]
                    toggle = not toggle
                    if toggle:
                        text_frame.grid(row=1, column=0,
                                        padx=0, pady=0, sticky=tk.NSEW)

                    else:
                        text_frame.grid_forget()
                    tk_widgets.LFI.loaded_list[file_frame_id][2] = toggle
                view_button = ctk.CTkButton(
                    top_file_frame,
                    text='+',
                    width=30,
                    command=lambda: view_cmd(file_frame_id)
                )
                view_button.grid(row=0, column=0, padx=2,
                                 pady=2, sticky=tk.W)
                # create file label
                file_label = ctk.CTkLabel(
                    top_file_frame,
                    text=f'[{size}] {path}',
                    anchor=tk.W,
                    justify=tk.LEFT
                )
                file_label.grid(row=0, column=1, padx=2,
                                pady=2, sticky=tk.W)
                # create search entry
                search_entry = ctk.CTkEntry(
                    top_file_frame,
                    placeholder_text='Search',
                    width=300
                )
                search_entry.grid(row=0, column=2, padx=0,
                                  pady=0, sticky=tk.E)

                def search_cmd(event, search_entry, file_frame_id):
                    textbox = tk_widgets.LFI.loaded_list[file_frame_id][4]
                    # reset hightlight
                    textbox.tag_remove('search', '1.0', tk.END)
                    pattern = search_entry.get()
                    if pattern == '':
                        # no pattern to search
                        return
                    # search from last search position if enter key else new search
                    return_key = event.char == '\r'
                    start_pos = tk_widgets.LFI.loaded_list[file_frame_id][5] if return_key else '1.0'
                    # first search
                    found_pos = textbox.search(
                        pattern,
                        start_pos,
                        nocase=True,
                        stopindex=tk.END,
                        forwards=True
                    )
                    if found_pos == '':
                        # if this search is trigger by enter key
                        # and last search position recorded
                        # but found empty,
                        # search again at 1.0 to cycle searching
                        if return_key and start_pos != '1.0':
                            found_pos = textbox.search(
                                pattern,
                                '1.0',
                                nocase=True,
                                stopindex=tk.END,
                                forwards=True
                            )
                            if found_pos == '':
                                # safe case because we search again
                                return
                        else:
                            # do nothing
                            return
                    # highlight pattern
                    end_pos = f'{found_pos} + {len(pattern)}c'
                    textbox.tag_config(
                        "search", background="grey")
                    textbox.tag_add('search', found_pos, end_pos)
                    # jump to see search pattern
                    textbox.see(found_pos)
                    # save search position
                    tk_widgets.LFI.loaded_list[file_frame_id][5] = end_pos

                search_entry.bind('<KeyRelease>', lambda event: search_cmd(
                    event, search_entry, file_frame_id))
                # create remove button

                def remove_cmd(file_frame_id):
                    if not tk_widgets.LFI.loaded_list[file_frame_id][6]:
                        file_frame = tk_widgets.LFI.loaded_list[file_frame_id][0]
                        file_frame.grid_forget()
                        file_frame.destroy()
                        tk_widgets.LFI.loaded_list[file_frame_id][6] = True

                remove_button = ctk.CTkButton(
                    top_file_frame,
                    text='X',
                    width=30,
                    command=lambda: remove_cmd(file_frame_id)
                )
                remove_button.grid(row=0, column=3, padx=2,
                                   pady=2, sticky=tk.W)
                # create bottom file frame
                bottom_file_frame = ctk.CTkFrame(
                    file_frame
                )
                bottom_file_frame.columnconfigure(0, weight=1)
                bottom_file_frame.rowconfigure(0, weight=1)
                # create file text
                file_text = ctk.CTkTextbox(
                    bottom_file_frame
                )
                file_text.insert('1.0', json)
                file_text.configure(
                    state=tk.DISABLED,
                    wrap=tk.NONE,
                    height=340
                )
                file_text.grid(row=0, column=0, padx=2,
                               pady=2, sticky=tk.NSEW)
                # add this file to list
                tk_widgets.LFI.loaded_list.append(
                    [
                        file_frame,
                        top_file_frame,
                        False,  # expand or not
                        bottom_file_frame,
                        file_text,
                        '1.0',  # text search pos
                        False  # deleted or not
                    ]
                )

            # create file read button

            def fileread_cmd():
                file_path = tkfd.askopenfilename(
                    title='Select League file',
                    filetypes=(
                        ('League files',
                            (
                                '*.bin',
                                '*.skl',
                                '*.skn',
                                '*.sco',
                                '*.scb',
                                '*.anm',
                                '*.mapgeo',
                                '*.bnk',
                                '*.wad.client'
                            )
                         ),
                        ('All files', '*.*')
                    )
                )
                if file_path != '':
                    Log.add(f'Running: Read {file_path}')
                    cdtb_hashes.CDTB.read_all()
                    read_file(file_path, cdtb_hashes.CDTB.HASHTABLES)
                    cdtb_hashes.CDTB.free_all()
                    Log.add(f'Done: Read {file_path}')
            tk_widgets.LFI.fileread_button = ctk.CTkButton(
                tk_widgets.LFI.input_frame,
                text='Read File',
                anchor=tk.CENTER,
                command=fileread_cmd
            )
            tk_widgets.LFI.fileread_button.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            # create folder read button

            def folderread_cmd():
                dir_path = tkfd.askdirectory(
                    title='Select Folder'
                )
                if dir_path != '':

                    Log.add(f'Running: Read {dir_path}')
                    cdtb_hashes.CDTB.read_all()
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(
                                root, file).replace('\\', '/')
                            read_file(
                                file_path, cdtb_hashes.CDTB.HASHTABLES, ignore_error=True)
                    cdtb_hashes.CDTB.free_all()
                    Log.add(f'Done: Read {dir_path}')
            tk_widgets.LFI.folderread_button = ctk.CTkButton(
                tk_widgets.LFI.input_frame,
                text='Read Folder',
                anchor=tk.CENTER,
                command=folderread_cmd
            )
            tk_widgets.LFI.folderread_button.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
            # create clear button

            def clear_cmd():
                loaded_file_count = len(tk_widgets.LFI.loaded_list)
                if loaded_file_count == 0:
                    return
                for loaded_file in tk_widgets.LFI.loaded_list:
                    if not loaded_file[6]:
                        file_frame = loaded_file[0]
                        file_frame.grid_forget()
                        file_frame.destroy()
                tk_widgets.LFI.loaded_list.clear()
                Log.add(f'Done: Cleared all loaded files.')
            tk_widgets.LFI.clear_button = ctk.CTkButton(
                tk_widgets.LFI.input_frame,
                text='Clear',
                anchor=tk.CENTER,
                command=clear_cmd
            )
            tk_widgets.LFI.clear_button.grid(
                row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

        tk_widgets.LFI.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 2:
        if tk_widgets.AMV.page_frame == None:
            tk_widgets.AMV.page_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame,
                fg_color=TRANSPARENT,
            )
            tk_widgets.AMV.page_frame.columnconfigure(0, weight=1)
            tk_widgets.AMV.page_frame.rowconfigure(0, weight=1)
            tk_widgets.AMV.page_frame.rowconfigure(1, weight=1)
            tk_widgets.AMV.page_frame.rowconfigure(2, weight=699)

            tk_widgets.AMV.table_loaded = False
            tk_widgets.AMV.bin_loaded = None

            # create input frame
            tk_widgets.AMV.input_frame = ctk.CTkFrame(
                tk_widgets.AMV.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.AMV.input_frame.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.AMV.input_frame.columnconfigure(0, weight=9)
            tk_widgets.AMV.input_frame.columnconfigure(1, weight=1)

            # create skl entry
            tk_widgets.AMV.skl_entry = ctk.CTkEntry(
                tk_widgets.AMV.input_frame,
            )
            tk_widgets.AMV.skl_entry.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            # create skl browse button

            def sklbrowse_cmd():
                skl_path = tkfd.askopenfilename(
                    title='Select SKL file',
                    filetypes=(
                        ('SKL files', '*.skl'),
                        ('All files', '*.*')
                    )
                )
                tk_widgets.AMV.skl_entry.delete(0, tk.END)
                tk_widgets.AMV.skl_entry.insert(tk.END, skl_path)
            tk_widgets.AMV.sklbrowse_button = ctk.CTkButton(
                tk_widgets.AMV.input_frame,
                text='Browse SKL',
                anchor=tk.CENTER,
                command=sklbrowse_cmd
            )
            tk_widgets.AMV.sklbrowse_button.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

            # create bin entry
            tk_widgets.AMV.bin_entry = ctk.CTkEntry(
                tk_widgets.AMV.input_frame,
            )
            tk_widgets.AMV.bin_entry.grid(
                row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

            def binbrowse_cmd():
                bin_path = tkfd.askopenfilename(
                    title='Select Animation BIN file',
                    filetypes=(
                        ('BIN files', ['*.bin']),
                        ('All files', '*.*')
                    )
                )
                tk_widgets.AMV.bin_entry.delete(0, tk.END)
                tk_widgets.AMV.bin_entry.insert(tk.END, bin_path)
            # create bin browse button
            tk_widgets.AMV.binbrowse_button = ctk.CTkButton(
                tk_widgets.AMV.input_frame,
                text='Browse Animation BIN',
                anchor=tk.CENTER,
                command=binbrowse_cmd
            )
            tk_widgets.AMV.binbrowse_button.grid(
                row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

            # create action frame
            tk_widgets.AMV.action_frame = ctk.CTkFrame(
                tk_widgets.AMV.page_frame, fg_color=TRANSPARENT)
            tk_widgets.AMV.action_frame.grid(
                row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.AMV.action_frame.columnconfigure(0, weight=1)
            tk_widgets.AMV.action_frame.columnconfigure(1, weight=1)
            tk_widgets.AMV.action_frame.columnconfigure(2, weight=1)
            tk_widgets.AMV.action_frame.columnconfigure(3, weight=699)

            # create load button
            def load_cmd():
                Log.add('Running: Load weight table')

                joint_names = []
                mask_names = []
                weights = []
                # read skl
                skl_path = tk_widgets.AMV.skl_entry.get()
                if skl_path != '':
                    Log.add(f'Running: Read {skl_path}')
                    skl_file = pyRitoFile.read_skl(skl_path)
                    Log.add(f'Done: Read {skl_path}')
                    joint_names = [joint.name for joint in skl_file.joints]
                # read bin
                bin_path = tk_widgets.AMV.bin_entry.get()
                if bin_path != '':
                    Log.add(f'Running: Read {bin_path}')
                    bin_file = pyRitoFile.read_bin(bin_path)
                    tk_widgets.AMV.bin_loaded = bin_file
                    Log.add(f'Done: Read {bin_path}')
                    mask_data = animask_viewer.get_weights(bin_file)
                    mask_names, weights = list(
                        mask_data.keys()), list(mask_data.values())

                # get table row and column length
                tk_widgets.AMV.table_row = len(joint_names)
                tk_widgets.AMV.table_column = len(mask_names)
                if tk_widgets.AMV.table_row == 0:
                    raise Exception(
                        'Failed: Load weight table: No joints found.')

                # create table frame
                if not tk_widgets.AMV.table_loaded:
                    # create horizontal scroll table frame
                    tk_widgets.AMV.htable_frame = ctk.CTkScrollableFrame(
                        tk_widgets.AMV.page_frame,
                        fg_color=TRANSPARENT,
                        orientation=ctk.HORIZONTAL
                    )
                    tk_widgets.AMV.htable_frame.rowconfigure(
                        0, weight=1)
                    tk_widgets.AMV.htable_frame.columnconfigure(
                        0, weight=1)

                    # create vertical scroll table frame
                    tk_widgets.AMV.vtable_frame = ctk.CTkScrollableFrame(
                        tk_widgets.AMV.htable_frame,
                        fg_color=TRANSPARENT,
                        orientation=ctk.VERTICAL
                    )
                    tk_widgets.AMV.vtable_frame.rowconfigure(
                        0, weight=1)
                    tk_widgets.AMV.vtable_frame.columnconfigure(
                        0, weight=1)
                else:
                    # hide the loaded table
                    tk_widgets.AMV.htable_frame.grid_forget()
                    tk_widgets.AMV.vtable_frame.grid_forget()
                    # destroy loaded table widgets
                    for widget in tk_widgets.AMV.table_widgets:
                        if widget != None:
                            widget.destroy()

                # update vertical/horizontal table frame's width (must)
                tk_widgets.AMV.htable_frame.configure(
                    width=170+(tk_widgets.AMV.table_column+1)*100
                )
                tk_widgets.AMV.vtable_frame.configure(
                    width=170+(tk_widgets.AMV.table_column+1)*100
                )

                # init empty table widgets
                tk_widgets.AMV.table_widgets = [
                    None]*((tk_widgets.AMV.table_row+1)*(tk_widgets.AMV.table_column+1))

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
                for j in range(tk_widgets.AMV.table_column+1):
                    for i in range(tk_widgets.AMV.table_row+1):
                        windex = i*(tk_widgets.AMV.table_column+1)+j
                        if windex == 0:
                            continue

                        # create mask name labels
                        if i == 0:
                            tk_widgets.AMV.table_widgets[windex] = ctk.CTkLabel(
                                tk_widgets.AMV.vtable_frame,
                                width=90,
                                text=mask_names[j-1]
                            )
                        # create joint name labels
                        elif j == 0:
                            tk_widgets.AMV.table_widgets[windex] = ctk.CTkLabel(
                                tk_widgets.AMV.vtable_frame,
                                width=160,
                                text=joint_names[i-1],
                                anchor=tk.W
                            )
                        # create weight entries
                        else:
                            tk_widgets.AMV.table_widgets[windex] = ctk.CTkEntry(
                                tk_widgets.AMV.vtable_frame,
                                width=80,
                                justify=tk.RIGHT,
                                validate='all',
                                validatecommand=(
                                    (tk_widgets.AMV.page_frame.register(
                                        validate_weight_cmd)),
                                    '%P'
                                )
                            )
                            # safe weight value if joints number > masks number
                            weight_value = '0'
                            try:
                                weight_value = f'{weights[j-1][i-1]:.3}'
                            except:
                                pass
                            tk_widgets.AMV.table_widgets[windex].insert(
                                tk.END, weight_value)
                        tk_widgets.AMV.table_widgets[windex].grid(
                            row=i, column=j, padx=5, pady=5, sticky=tk.NSEW)

                # show the table
                tk_widgets.AMV.htable_frame.grid(row=2, column=0, padx=5,
                                                 pady=5, sticky=tk.NSEW)
                tk_widgets.AMV.vtable_frame.grid(
                    row=0, column=0, sticky=tk.NSEW)
                # mark as table loaded
                tk_widgets.AMV.table_loaded = True
                Log.add('Done: Load weight table')
            tk_widgets.AMV.load_button = ctk.CTkButton(
                tk_widgets.AMV.action_frame,
                text='Load',
                command=load_cmd
            )
            tk_widgets.AMV.load_button.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

            # create save button
            def save_cmd():
                if not tk_widgets.AMV.table_loaded:
                    return

                # save to txt file (bin later)
                bin_path = tkfd.asksaveasfilename(
                    title='Select output Animation BIN path',
                    filetypes=(
                        ('BIN files', '*.bin'),
                        ('All files', '*.*')
                    ),
                    defaultextension='.bin'
                )
                if bin_path == '':
                    return

                # dump [(mask, weights),...]
                # start from column 1 because column 0 is just joint names
                mask_data = {}
                for j in range(1, tk_widgets.AMV.table_column+1):
                    mask_name = None
                    weights = []
                    for i in range(tk_widgets.AMV.table_row+1):
                        windex = i*(tk_widgets.AMV.table_column+1)+j
                        if windex == 0:
                            continue

                        # first row = mask names
                        if i == 0:
                            mask_name = tk_widgets.AMV.table_widgets[windex].cget(
                                'text')
                        else:
                            weight = tk_widgets.AMV.table_widgets[windex].get(
                            )
                            weights.append(float(weight))

                    mask_data[mask_name] = weights

                # set weights and save bin
                bin_file = tk_widgets.AMV.bin_loaded
                animask_viewer.set_weights(bin_file, mask_data)
                pyRitoFile.write_bin(bin_path, bin_file)
            tk_widgets.AMV.save_button = ctk.CTkButton(
                tk_widgets.AMV.action_frame,
                text='Save As',
                command=save_cmd
            )
            tk_widgets.AMV.save_button.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

            # create clear button
            def clear_cmd():
                Log.add('Running: Clear weight table')
                if not tk_widgets.AMV.table_loaded:
                    return
                # destroy tk widgets
                for widget in tk_widgets.AMV.table_widgets:
                    if widget != None:
                        widget.destroy()
                tk_widgets.AMV.vtable_frame.grid_forget()
                tk_widgets.AMV.htable_frame.grid_forget()
                tk_widgets.AMV.bin_loaded = None
                tk_widgets.AMV.table_loaded = False
                Log.add('Done: Clear weight table')
            tk_widgets.AMV.clear_button = ctk.CTkButton(
                tk_widgets.AMV.action_frame,
                text='Clear',
                command=clear_cmd
            )
            tk_widgets.AMV.clear_button.grid(
                row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

        tk_widgets.AMV.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 3:
        pass
    elif selected == 4:
        # Log
        tk_widgets.LOG.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 5:
        pass


def create_mini_log():
    tk_widgets.mainbottom_frame.columnconfigure(0, weight=1)
    tk_widgets.mainbottom_frame.rowconfigure(0, weight=1)
    tk_widgets.mainbottom_frame.rowconfigure(1, weight=1)
    tk_widgets.bottom_widgets = Keeper()

    # create mini log
    tk_widgets.bottom_widgets.minilog_label = ctk.CTkLabel(
        tk_widgets.mainbottom_frame,
        text='',
        anchor=tk.W,
        justify=tk.CENTER
    )
    tk_widgets.bottom_widgets.minilog_label.grid(
        row=0, column=0, padx=10, pady=0, sticky=tk.NSEW)

    tk_widgets.bottom_widgets.minilog_label.bind(
        '<Button-1>',
        lambda event: tk_widgets.select_control(4)
    )
    Log.minilog_label = tk_widgets.bottom_widgets.minilog_label


# init variable
TRANSPARENT = 'transparent'
ctk.set_appearance_mode('system')
tk_widgets = Keeper()


# redirect tkinter error print
def rce(self, *args):
    err = format_exception(*args)
    Log.add(err)
    print(''.join(err))


ctk.CTk.report_callback_exception = rce


def start():
    # create UI
    create_main_app_and_frames()
    create_page_controls()
    create_mini_log()

    cdtb_hashes.CDTB.LOG = Log.add
    cdtb_hashes.CDTB.sync_in_thread()

    # loop the UI
    tk_widgets.main_tk.mainloop()
