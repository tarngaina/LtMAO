
import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as tkfd

from LtMAO import setting, pyRitoFile, wad_tool, hash_manager, leaguefile_inspector, animask_viewer, no_skin, uvee
from LtMAO.prettyUI.helper import Keeper, Log

import os
import os.path
from threading import Thread
from traceback import format_exception

# transparent color
TRANSPARENT = 'transparent'
# to keep all created widgets
tk_widgets = Keeper()


def rce(self, *args):
    # redirect tkinter error print
    err = format_exception(*args)
    Log.add(err)
    print(''.join(err))


ctk.CTk.report_callback_exception = rce


def check_thread_safe(thread):
    if thread == None:
        return True
    else:
        if not thread.is_alive():
            return True
    return False


def create_main_app_and_frames():
    # create main app
    tk_widgets.main_tk = ctk.CTk()
    tk_widgets.main_tk.geometry('1000x620')
    tk_widgets.main_tk.title('LtMAO')
    # create main top-bottom frame
    tk_widgets.main_tk.rowconfigure(0, weight=100)
    tk_widgets.main_tk.rowconfigure(1, weight=1)
    tk_widgets.main_tk.columnconfigure(0, weight=1)
    tk_widgets.maintop_frame = ctk.CTkFrame(
        tk_widgets.main_tk,
        fg_color=TRANSPARENT
    )
    tk_widgets.maintop_frame.grid(
        row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    tk_widgets.mainbottom_frame = ctk.CTkFrame(
        tk_widgets.main_tk,
        height=30
    )
    tk_widgets.mainbottom_frame.grid(
        row=1, column=0, padx=0, pady=2, sticky=tk.NSEW)
    # create main top left-right frame
    tk_widgets.maintop_frame.rowconfigure(0, weight=1)
    tk_widgets.maintop_frame.columnconfigure(0, weight=0)
    tk_widgets.maintop_frame.columnconfigure(1, weight=1)
    tk_widgets.mainleft_frame = ctk.CTkFrame(
        tk_widgets.maintop_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.mainleft_frame.grid(
        row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    tk_widgets.mainright_frame = ctk.CTkFrame(
        tk_widgets.maintop_frame
    )
    tk_widgets.mainright_frame.grid(
        row=0, column=1, padx=0, pady=0, sticky=tk.NSEW)


def create_page_controls():
    tk_widgets.mainright_frame.columnconfigure(0, weight=1)
    tk_widgets.mainright_frame.rowconfigure(0, weight=1)
    tk_widgets.mainleft_frame.columnconfigure(0, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(0, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(1, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(2, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(3, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(4, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(5, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(6, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(7, weight=699)
    tk_widgets.mainleft_frame.rowconfigure(8, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(9, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(10, weight=1)

    # create left controls buttons
    def control_cmd(page):
        # update control display
        for id, control_button in enumerate(tk_widgets.control_buttons):
            if id == page:
                control_button.configure(
                    fg_color=tk_widgets.c_active_fg,
                    text_color=tk_widgets.c_active_text
                )
            else:
                control_button.configure(
                    fg_color=tk_widgets.c_nonactive_fg,
                    text_color=tk_widgets.c_nonactive_text
                )
        # show page
        select_right_page(page)
    # create left control
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
            text='hash_manager',
            command=lambda: control_cmd(3)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='vo_helper',
            command=lambda: control_cmd(4)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='no_skin',
            command=lambda: control_cmd(5)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='uvee',
            command=lambda: control_cmd(6)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='bin_helper',
            command=lambda: control_cmd(7)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='Log',
            command=lambda: control_cmd(8)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='Setting',
            command=lambda: control_cmd(9)
        )
    ]
    for id, control_button in enumerate(tk_widgets.control_buttons):
        control_button.grid(
            row=id, column=0, padx=5, pady=5, sticky=tk.N+tk.EW)
    # get color for controls
    temp_button = ctk.CTkButton(None)
    tk_widgets.c_active_fg = temp_button.cget('fg_color')
    tk_widgets.c_nonactive_fg = TRANSPARENT
    tk_widgets.c_active_text = temp_button.cget('text_color')
    tk_widgets.c_nonactive_text = ctk.CTkLabel(None).cget('text_color')
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
    tk_widgets.HM = tk_widgets.pages[3]
    tk_widgets.NS = tk_widgets.pages[5]
    tk_widgets.UVEE = tk_widgets.pages[6]
    tk_widgets.LOG = tk_widgets.pages[8]
    tk_widgets.ST = tk_widgets.pages[9]
    # create Log page
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
    Log.tk_log = tk_widgets.LOG.log_textbox
    # select first page
    tk_widgets.select_control(0)


def select_right_page(selected):
    # hide other page
    for page in tk_widgets.pages:
        if page.page_frame != None:
            page.page_frame.grid_forget()
    # create/show selected page
    if selected == 0:
        pass
    elif selected == 1:
        if tk_widgets.LFI.page_frame == None:
            # create page frame
            tk_widgets.LFI.page_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame,
                fg_color=TRANSPARENT,
            )
            tk_widgets.LFI.page_frame.columnconfigure(0, weight=1)
            tk_widgets.LFI.page_frame.rowconfigure(0, weight=1)
            tk_widgets.LFI.page_frame.rowconfigure(1, weight=699)
            # init stuffs
            tk_widgets.LFI.loaded_files = []
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
                path, size, json = leaguefile_inspector.read_json(
                    file_path, hastables, ignore_error)
                if json == None:
                    return
                # id of this file
                file_frame_id = len(tk_widgets.LFI.loaded_files)
                # create file frame
                file_frame = ctk.CTkFrame(
                    tk_widgets.LFI.view_frame
                )
                file_frame.grid(row=file_frame_id, column=0,
                                padx=2, pady=5, sticky=tk.NSEW)
                file_frame.columnconfigure(0, weight=1)
                file_frame.rowconfigure(0, weight=1)
                # create head frame
                head_frame = ctk.CTkFrame(
                    file_frame
                )
                head_frame.grid(row=0, column=0,
                                padx=0, pady=0, sticky=tk.NSEW)
                head_frame.columnconfigure(0, weight=0)
                head_frame.columnconfigure(1, weight=1)
                head_frame.columnconfigure(2, weight=0)
                head_frame.columnconfigure(3, weight=0)
                head_frame.rowconfigure(0, weight=1)

                def view_cmd(file_frame_id):
                    toggle = tk_widgets.LFI.loaded_files[file_frame_id][2]
                    content_frame = tk_widgets.LFI.loaded_files[file_frame_id][3]
                    toggle = not toggle
                    if toggle:
                        content_frame.grid(row=1, column=0,
                                           padx=0, pady=0, sticky=tk.NSEW)

                    else:
                        content_frame.grid_forget()
                    tk_widgets.LFI.loaded_files[file_frame_id][2] = toggle
                # create view button
                view_button = ctk.CTkButton(
                    head_frame,
                    text='+',
                    width=30,
                    command=lambda: view_cmd(file_frame_id)
                )
                view_button.grid(row=0, column=0, padx=2,
                                 pady=2, sticky=tk.W)
                # create file label
                file_label = ctk.CTkLabel(
                    head_frame,
                    text=f'[{size}] {path}',
                    anchor=tk.W,
                    justify=tk.LEFT
                )
                file_label.grid(row=0, column=1, padx=2,
                                pady=2, sticky=tk.W)
                # create search entry
                search_entry = ctk.CTkEntry(
                    head_frame,
                    placeholder_text='Search',
                    width=300
                )
                search_entry.grid(row=0, column=2, padx=0,
                                  pady=0, sticky=tk.E)

                def search_cmd(event, search_entry, file_frame_id):
                    file_text = tk_widgets.LFI.loaded_files[file_frame_id][4]
                    # reset hightlight
                    file_text.tag_remove('search', '1.0', tk.END)
                    pattern = search_entry.get()
                    if pattern == '':
                        # no pattern to search
                        return
                    # search from last search position if enter key else new search
                    return_key = event.char == '\r'
                    start_pos = tk_widgets.LFI.loaded_files[file_frame_id][5] if return_key else '1.0'
                    # first search
                    found_pos = file_text.search(
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
                            found_pos = file_text.search(
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
                    file_text.tag_config(
                        "search", background="grey")
                    file_text.tag_add('search', found_pos, end_pos)
                    # set view
                    file_text.see(found_pos)
                    # save search position
                    tk_widgets.LFI.loaded_files[file_frame_id][5] = end_pos

                search_entry.bind('<KeyRelease>', lambda event: search_cmd(
                    event, search_entry, file_frame_id))

                def remove_cmd(file_frame_id):
                    if not tk_widgets.LFI.loaded_files[file_frame_id][6]:
                        file_frame = tk_widgets.LFI.loaded_files[file_frame_id][0]
                        file_frame.grid_forget()
                        file_frame.destroy()
                        tk_widgets.LFI.loaded_files[file_frame_id][6] = True
                # create remove button
                remove_button = ctk.CTkButton(
                    head_frame,
                    text='X',
                    width=30,
                    command=lambda: remove_cmd(file_frame_id)
                )
                remove_button.grid(row=0, column=3, padx=2,
                                   pady=2, sticky=tk.W)
                # create bottom file frame
                content_frame = ctk.CTkFrame(
                    file_frame
                )
                content_frame.columnconfigure(0, weight=1)
                content_frame.rowconfigure(0, weight=1)
                # create file text
                file_text = ctk.CTkTextbox(
                    content_frame
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
                tk_widgets.LFI.loaded_files.append(
                    [
                        file_frame,
                        head_frame,
                        False,  # expand or not
                        content_frame,
                        file_text,
                        '1.0',  # text search pos
                        False  # deleted or not
                    ]
                )

            def fileread_cmd():
                file_paths = tkfd.askopenfilenames(
                    title='Select League Files To Read',
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
                if len(file_paths) > 0:
                    hash_manager.read_all_hashes()
                    for file_path in file_paths:
                        read_file(
                            file_path, hash_manager.HASHTABLES)
                    hash_manager.free_all_hashes()
            # create file read button
            tk_widgets.LFI.fileread_button = ctk.CTkButton(
                tk_widgets.LFI.input_frame,
                text='Read Files',
                anchor=tk.CENTER,
                command=fileread_cmd
            )
            tk_widgets.LFI.fileread_button.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

            def folderread_cmd():
                dir_path = tkfd.askdirectory(
                    title='Select Folder To Read'
                )
                if dir_path != '':
                    hash_manager.read_all_hashes()
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(
                                root, file).replace('\\', '/')
                            read_file(
                                file_path, hash_manager.HASHTABLES, ignore_error=True)
                    hash_manager.free_all_hashes()
            # create folder read button
            tk_widgets.LFI.folderread_button = ctk.CTkButton(
                tk_widgets.LFI.input_frame,
                text='Read Folder',
                anchor=tk.CENTER,
                command=folderread_cmd
            )
            tk_widgets.LFI.folderread_button.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

            def clear_cmd():
                loaded_file_count = len(tk_widgets.LFI.loaded_files)
                if loaded_file_count == 0:
                    return
                for loaded_file in tk_widgets.LFI.loaded_files:
                    if not loaded_file[6]:
                        file_frame = loaded_file[0]
                        file_frame.grid_forget()
                        file_frame.destroy()
                tk_widgets.LFI.loaded_files.clear()
                Log.add(f'Done: Cleared all loaded files.')
            # create clear button
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
        if tk_widgets.HM.page_frame == None:
            tk_widgets.HM.page_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame,
                fg_color=TRANSPARENT,
            )
            tk_widgets.HM.page_frame.columnconfigure(0, weight=1)
            tk_widgets.HM.page_frame.rowconfigure(0, weight=1)
            tk_widgets.HM.page_frame.rowconfigure(1, weight=1)
            tk_widgets.HM.page_frame.rowconfigure(2, weight=699)

            tk_widgets.HM.extracting_thread = None

            # create info frame
            tk_widgets.HM.info_frame = ctk.CTkFrame(
                tk_widgets.HM.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.HM.info_frame.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.HM.info_frame.columnconfigure(0, weight=1)
            tk_widgets.HM.info_frame.columnconfigure(1, weight=0)
            tk_widgets.HM.info_frame.columnconfigure(2, weight=699)
            tk_widgets.HM.info_frame.rowconfigure(0, weight=1)

            folder_label_text = [
                f'CDTB: {hash_manager.CDTB.local_dir}',
                f'Extracted: {hash_manager.ExtractedHashes.local_dir}',
                f'Custom: {hash_manager.CustomHashes.local_dir}'
            ]

            def folder_cmd(index):
                if index == 0:
                    os.startfile(os.path.abspath(
                        hash_manager.CDTB.local_dir))
                elif index == 1:
                    os.startfile(os.path.abspath(
                        hash_manager.ExtractedHashes.local_dir))
                else:
                    os.startfile(os.path.abspath(
                        hash_manager.CustomHashes.local_dir))
            for i in range(3):
                folder_label = ctk.CTkLabel(
                    tk_widgets.HM.info_frame,
                    text=folder_label_text[i],
                    anchor=tk.W
                )
                folder_label.grid(row=i, column=0, padx=5,
                                  pady=5, sticky=tk.NSEW)
                folder_button = ctk.CTkButton(
                    tk_widgets.HM.info_frame,
                    text='Open',
                    command=lambda index=i: folder_cmd(index)
                )
                folder_button.grid(row=i, column=1, padx=5,
                                   pady=5, sticky=tk.NSEW)

            # create input frame
            tk_widgets.HM.input_frame = ctk.CTkFrame(
                tk_widgets.HM.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.HM.input_frame.grid(
                row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.HM.input_frame.rowconfigure(0, weight=1)
            tk_widgets.HM.input_frame.columnconfigure(0, weight=1)
            tk_widgets.HM.input_frame.columnconfigure(1, weight=1)
            tk_widgets.HM.input_frame.columnconfigure(2, weight=699)

            # create file read button
            def fileextract_cmd():
                if check_thread_safe(tk_widgets.HM.extracting_thread):
                    file_paths = tkfd.askopenfilenames(
                        title='Select WAD/BIN/SKN/SKL File To Extract',
                        filetypes=(
                            ('League files',
                                (
                                    '*.wad.client',
                                    '*.bin',
                                    '*.skn',
                                    '*.skl'
                                )
                             ),
                            ('All files', '*.*')
                        )
                    )
                    if len(file_paths) > 0:
                        tk_widgets.HM.extracting_thread = Thread(
                            target=lambda: hash_manager.ExtractedHashes.extract(
                                *file_paths),
                            daemon=True
                        )
                        tk_widgets.HM.extracting_thread.start()
                else:
                    Log.add(
                        'Failed: Extract Hashes: A thread is already running, wait for it to finished.')

            tk_widgets.HM.fileread_button = ctk.CTkButton(
                tk_widgets.HM.input_frame,
                text='Extract From Files',
                anchor=tk.CENTER,
                command=fileextract_cmd
            )
            tk_widgets.HM.fileread_button.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

            # create folder read button
            def folderextract_cmd():
                if check_thread_safe(tk_widgets.HM.extracting_thread):
                    dir_path = tkfd.askdirectory(
                        title='Select Folder To Extract',
                    )
                    if dir_path != '':
                        file_paths = []
                        for root, dirs, files in os.walk(dir_path):
                            for file in files:
                                file_paths.append(os.path.join(
                                    root, file).replace('\\', '/'))
                        if len(file_paths) > 0:
                            tk_widgets.HM.extracting_thread = Thread(
                                target=lambda: hash_manager.ExtractedHashes.extract(
                                    *file_paths),
                                daemon=True
                            )
                            tk_widgets.HM.extracting_thread.start()
                else:
                    Log.add(
                        'Failed: Extract Hashes: A thread is already running, wait for it to finished.')

            tk_widgets.HM.folderread_button = ctk.CTkButton(
                tk_widgets.HM.input_frame,
                text='Extract From Folder',
                anchor=tk.CENTER,
                command=folderextract_cmd
            )
            tk_widgets.HM.folderread_button.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

        tk_widgets.HM.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 4:
        pass
    elif selected == 5:
        if tk_widgets.NS.page_frame == None:
            # create page frame
            tk_widgets.NS.page_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame,
                fg_color=TRANSPARENT,
            )
            tk_widgets.NS.page_frame.columnconfigure(0, weight=1)
            tk_widgets.NS.page_frame.rowconfigure(0, weight=1)
            tk_widgets.NS.page_frame.rowconfigure(1, weight=1)
            tk_widgets.NS.page_frame.rowconfigure(2, weight=699)
            # init stuffs
            tk_widgets.NS.working_thread = None
            # create input frame
            tk_widgets.NS.input_frame = ctk.CTkFrame(
                tk_widgets.NS.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.NS.input_frame.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.NS.input_frame.columnconfigure(0, weight=9)
            tk_widgets.NS.input_frame.columnconfigure(1, weight=1)
            # create champions folder entry
            tk_widgets.NS.cfolder_entry = ctk.CTkEntry(
                tk_widgets.NS.input_frame,
            )
            tk_widgets.NS.cfolder_entry.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

            def browse_cmd():
                skl_path = tkfd.askdirectory(
                    title='Select Folder: League of Legends/Game/DATA/FINAL/Champions',
                )
                tk_widgets.NS.cfolder_entry.delete(0, tk.END)
                tk_widgets.NS.cfolder_entry.insert(tk.END, skl_path)
            # create browse button
            tk_widgets.NS.browse_button = ctk.CTkButton(
                tk_widgets.NS.input_frame,
                text='Browse Champions folder',
                anchor=tk.CENTER,
                command=browse_cmd
            )
            tk_widgets.NS.browse_button.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
            # create action frame
            tk_widgets.NS.action_frame = ctk.CTkFrame(
                tk_widgets.NS.page_frame, fg_color=TRANSPARENT)
            tk_widgets.NS.action_frame.grid(
                row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.NS.action_frame.columnconfigure(0, weight=1)
            tk_widgets.NS.action_frame.columnconfigure(1, weight=699)
            tk_widgets.NS.action_frame.columnconfigure(2, weight=1)

            def save_skips_cmd():
                no_skin.set_skips(
                    tk_widgets.NS.skips_textbox.get('1.0', tk.END))
                no_skin.save_skips()
                Log.add('Done: Save SKIPS.json')
            # create save SKIPS button
            tk_widgets.NS.save_skips_button = ctk.CTkButton(
                tk_widgets.NS.action_frame,
                text='Save SKIPS',
                command=save_skips_cmd
            )
            tk_widgets.NS.save_skips_button.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

            def start_cmd():
                if check_thread_safe(tk_widgets.NS.working_thread):
                    dir_path = tkfd.askdirectory(
                        title='Select Output Folder'
                    )
                    if dir_path != '':
                        tk_widgets.NS.working_thread = Thread(
                            target=no_skin.parse,
                            args=(tk_widgets.NS.cfolder_entry.get(),),
                            daemon=True
                        )
                        tk_widgets.NS.working_thread.start()
                else:
                    Log.add(
                        'Failed: Create NO SKIN mod: A thread is already running, wait for it to finished.')
            # create start button
            tk_widgets.NS.start_button = ctk.CTkButton(
                tk_widgets.NS.action_frame,
                text='Start',
                command=start_cmd
            )
            tk_widgets.NS.start_button.grid(
                row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
            # create skips textbox
            tk_widgets.NS.skips_textbox = ctk.CTkTextbox(
                tk_widgets.NS.page_frame,
                wrap=tk.NONE
            )
            def tab_pressed():
                tk_widgets.NS.skips_textbox.insert('insert', ' '*4)
                return 'break'
            tk_widgets.NS.skips_textbox.bind(
                '<Tab>', lambda e: tab_pressed())
            tk_widgets.NS.skips_textbox.insert(tk.END, no_skin.get_skips())
            tk_widgets.NS.skips_textbox.grid(
                row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
        tk_widgets.NS.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 6:
        if tk_widgets.UVEE.page_frame == None:
            # create page frame
            tk_widgets.UVEE.page_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame,
                fg_color=TRANSPARENT,
            )
            tk_widgets.UVEE.page_frame.columnconfigure(0, weight=1)
            tk_widgets.UVEE.page_frame.rowconfigure(0, weight=1)
            tk_widgets.UVEE.page_frame.rowconfigure(1, weight=699)
            # init stuffs
            tk_widgets.UVEE.loaded_files = []
            # create input frame
            tk_widgets.UVEE.input_frame = ctk.CTkFrame(
                tk_widgets.UVEE.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.UVEE.input_frame.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
            tk_widgets.UVEE.input_frame.rowconfigure(0, weight=1)
            tk_widgets.UVEE.input_frame.columnconfigure(0, weight=1)
            tk_widgets.UVEE.input_frame.columnconfigure(1, weight=1)
            tk_widgets.UVEE.input_frame.columnconfigure(2, weight=1)
            tk_widgets.UVEE.input_frame.columnconfigure(3, weight=1)
            tk_widgets.UVEE.input_frame.columnconfigure(4, weight=699)
            # create view frame
            tk_widgets.UVEE.view_frame = ctk.CTkScrollableFrame(
                tk_widgets.UVEE.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.UVEE.view_frame.grid(
                row=1, column=0, padx=0, pady=0, sticky=tk.NSEW)
            tk_widgets.UVEE.view_frame.columnconfigure(0, weight=1)
            # read one file function

            def read_file(file_path):
                uvee_imgs = uvee.uvee_file(file_path)
                if uvee_imgs == None or not tk_widgets.UVEE.load_extracted_files:
                    return
                # id of this file
                file_frame_id = len(tk_widgets.UVEE.loaded_files)
                # create file frame
                file_frame = ctk.CTkFrame(
                    tk_widgets.UVEE.view_frame
                )
                file_frame.grid(row=file_frame_id, column=0,
                                padx=2, pady=5, sticky=tk.NSEW)
                file_frame.columnconfigure(0, weight=1)
                file_frame.rowconfigure(0, weight=1)
                # create head frame
                head_frame = ctk.CTkFrame(
                    file_frame
                )
                head_frame.grid(row=0, column=0,
                                padx=0, pady=0, sticky=tk.NSEW)
                head_frame.columnconfigure(0, weight=0)
                head_frame.columnconfigure(1, weight=1)
                head_frame.columnconfigure(2, weight=0)
                head_frame.columnconfigure(3, weight=0)
                head_frame.rowconfigure(0, weight=1)

                def view_cmd(file_frame_id):
                    toggle = tk_widgets.UVEE.loaded_files[file_frame_id][2]
                    content_frame = tk_widgets.UVEE.loaded_files[file_frame_id][3]
                    toggle = not toggle
                    if toggle:
                        content_frame.grid(row=1, column=0,
                                           padx=0, pady=0, sticky=tk.NSEW)
                    else:
                        content_frame.grid_forget()
                    tk_widgets.UVEE.loaded_files[file_frame_id][2] = toggle
                # create view button
                view_button = ctk.CTkButton(
                    head_frame,
                    text='+',
                    width=30,
                    command=lambda: view_cmd(file_frame_id)
                )
                view_button.grid(row=0, column=0, padx=2,
                                 pady=2, sticky=tk.W)
                # create file label
                file_label = ctk.CTkLabel(
                    head_frame,
                    text=file_path,
                    anchor=tk.W,
                    justify=tk.LEFT
                )
                file_label.grid(row=0, column=1, padx=2,
                                pady=2, sticky=tk.W)

                def remove_cmd(file_frame_id):
                    if not tk_widgets.UVEE.loaded_files[file_frame_id][4]:
                        file_frame = tk_widgets.UVEE.loaded_files[file_frame_id][0]
                        file_frame.grid_forget()
                        file_frame.destroy()
                        tk_widgets.UVEE.loaded_files[file_frame_id][4] = True
                # create remove button
                remove_button = ctk.CTkButton(
                    head_frame,
                    text='X',
                    width=30,
                    command=lambda: remove_cmd(file_frame_id)
                )
                remove_button.grid(row=0, column=3, padx=2,
                                   pady=2, sticky=tk.W)
                # create bottom file frame
                content_frame = ctk.CTkFrame(
                    file_frame,
                    height=len(uvee_imgs) * (512+30)
                )
                for id, (uv_name, uv_img) in enumerate(uvee_imgs):
                    uv_image_label = ctk.CTkLabel(
                        content_frame,
                        text=f'[{id}] {uv_name}',
                        image=ctk.CTkImage(uv_img.resize(
                            (512, 512)), size=(512, 512)),
                        compound=tk.BOTTOM,
                        anchor=tk.W,
                        justify=tk.LEFT,
                        fg_color='black'
                    )
                    uv_image_label.grid(
                        row=id, column=0, padx=2, pady=2)
                # add this file to list
                tk_widgets.UVEE.loaded_files.append(
                    [
                        file_frame,
                        head_frame,
                        False,  # expand or not
                        content_frame,
                        False  # deleted or not
                    ]
                )

            def fileread_cmd():
                file_paths = tkfd.askopenfilenames(
                    title='Select SKN/SCO/SCB File To Extract',
                    filetypes=(
                        ('SKN/SCO/SCB files',
                            (
                                '*.skn',
                                '*.sco',
                                '*.scb',
                            )
                         ),
                        ('All files', '*.*')
                    )
                )
                if len(file_paths) > 0:
                    for file_path in file_paths:
                        read_file(file_path)
            # create file read button
            tk_widgets.UVEE.fileread_button = ctk.CTkButton(
                tk_widgets.UVEE.input_frame,
                text='Extract UVs From Files',
                anchor=tk.CENTER,
                command=fileread_cmd
            )
            tk_widgets.UVEE.fileread_button.grid(
                row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

            def folderread_cmd():
                dir_path = tkfd.askdirectory(
                    title='Select Folder To Extract'
                )
                if dir_path != '':
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(
                                root, file).replace('\\', '/')
                            read_file(file_path)
            # create folder read button
            tk_widgets.UVEE.folderread_button = ctk.CTkButton(
                tk_widgets.UVEE.input_frame,
                text='Extract UVs From Folder',
                anchor=tk.CENTER,
                command=folderread_cmd
            )
            tk_widgets.UVEE.folderread_button.grid(
                row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

            def clear_cmd():
                loaded_file_count = len(tk_widgets.UVEE.loaded_files)
                if loaded_file_count == 0:
                    return
                for loaded_file in tk_widgets.UVEE.loaded_files:
                    if not loaded_file[4]:
                        file_frame = loaded_file[0]
                        file_frame.grid_forget()
                        file_frame.destroy()
                tk_widgets.UVEE.loaded_files.clear()
                Log.add(f'Done: Cleared all loaded images.')
            # create clear button
            tk_widgets.UVEE.clear_button = ctk.CTkButton(
                tk_widgets.UVEE.input_frame,
                text='Clear Loaded Images',
                anchor=tk.CENTER,
                command=clear_cmd
            )
            tk_widgets.UVEE.clear_button.grid(
                row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

            def lef_cmd():
                tk_widgets.UVEE.load_extracted_files = tk_widgets.UVEE.lef_switch.get() == 1
                setting.set('Uvee.load_extracted_files',
                            tk_widgets.UVEE.load_extracted_files)
                setting.save()
            # create load extracted files switch
            tk_widgets.UVEE.lef_switch = ctk.CTkSwitch(
                tk_widgets.UVEE.input_frame,
                text='Load extracted files',
                command=lef_cmd
            )
            tk_widgets.UVEE.load_extracted_files = setting.get(
                'Uvee.load_extracted_files', False)
            if tk_widgets.UVEE.load_extracted_files:
                tk_widgets.UVEE.lef_switch.select()
            else:
                tk_widgets.UVEE.lef_switch.deselect()
            tk_widgets.UVEE.lef_switch.grid(
                row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)

        tk_widgets.UVEE.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 7:
        pass
    elif selected == 8:
        # Log
        tk_widgets.LOG.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 9:
        # Setting
        if tk_widgets.ST.page_frame == None:
            tk_widgets.ST.page_frame = ctk.CTkFrame(
                tk_widgets.mainright_frame,
                fg_color=TRANSPARENT,
            )
            tk_widgets.ST.page_frame.columnconfigure(0, weight=1)
            tk_widgets.ST.page_frame.rowconfigure(0, weight=1)

            tk_widgets.ST.scroll_frame = ctk.CTkScrollableFrame(
                tk_widgets.ST.page_frame,
                fg_color=TRANSPARENT
            )
            tk_widgets.ST.scroll_frame.grid(
                row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)

            # general
            tk_widgets.ST.general_label = ctk.CTkLabel(
                tk_widgets.ST.scroll_frame,
                text='General',
                anchor=tk.W
            )
            tk_widgets.ST.general_label.grid(
                row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

            # theme
            tk_widgets.ST.theme_label = ctk.CTkLabel(
                tk_widgets.ST.scroll_frame,
                text='Theme:',
                anchor=tk.W
            )
            tk_widgets.ST.theme_label.grid(
                row=1, column=0, padx=20, pady=5, sticky=tk.NSEW)

            def theme_cmd(choice):
                ctk.set_appearance_mode(choice)
                setting.set('theme', choice)
                setting.save()
            tk_widgets.ST.theme_option = ctk.CTkOptionMenu(
                tk_widgets.ST.scroll_frame,
                values=[
                    'light',
                    'dark',
                    'system'
                ],
                command=theme_cmd
            )
            tk_widgets.ST.theme_option.set(setting.get('theme', 'system'))
            tk_widgets.ST.theme_option.grid(
                row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

            # log
            tk_widgets.ST.log_label = ctk.CTkLabel(
                tk_widgets.ST.scroll_frame,
                text='Log',
                anchor=tk.W
            )
            tk_widgets.ST.log_label.grid(
                row=2, column=0, padx=10, pady=10, sticky=tk.NSEW)
            # limit message
            tk_widgets.ST.loglimit_label = ctk.CTkLabel(
                tk_widgets.ST.scroll_frame,
                text='Limit Messages:',
                anchor=tk.W
            )
            tk_widgets.ST.loglimit_label.grid(
                row=3, column=0, padx=20, pady=5, sticky=tk.NSEW)

            def loglimit_cmd(choice):
                Log.limit = int(choice)
                setting.set('Log.limit', choice)
                setting.save()
            tk_widgets.ST.loglimit_option = ctk.CTkOptionMenu(
                tk_widgets.ST.scroll_frame,
                values=[
                    '100',
                    '1000',
                    '10000'
                ],
                command=loglimit_cmd
            )
            tk_widgets.ST.loglimit_option.set(setting.get('Log.limit', '100'))
            tk_widgets.ST.loglimit_option.grid(
                row=3, column=1, padx=5, pady=5, sticky=tk.NSEW)

        tk_widgets.ST.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)


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
        lambda event: tk_widgets.select_control(8)
    )
    Log.tk_minilog = tk_widgets.bottom_widgets.minilog_label


def start():
    # create UI
    create_main_app_and_frames()
    create_page_controls()
    create_mini_log()

    # prepare and override settings
    setting.prepare(Log.add)
    ctk.set_appearance_mode(setting.get('theme', 'system'))
    Log.limit = int(setting.get('Log.limit', '100'))
    wad_tool.prepare(Log.add)
    hash_manager.prepare(Log.add)
    leaguefile_inspector.prepare(Log.add)
    no_skin.prepare(Log.add)
    uvee.prepare(Log.add)

    # loop the UI
    tk_widgets.main_tk.mainloop()
