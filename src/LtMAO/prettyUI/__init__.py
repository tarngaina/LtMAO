
import customtkinter as ctk
import tkinterdnd2 as tkdnd
import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.ttk as ttk
import pywinstyles
import requests

from .. import setting, pyRitoFile, winLT, wad_tool, hash_manager, cslmao, leaguefile_inspector, animask_viewer, no_skin, vo_helper, uvee, ext_tools, shrum, pyntex, hapiBin, bnk_tool, sborf, lol2fbx, Ritoddstex
from ..prettyUI.helper import Keeper, Log, EmojiImage, check_thread_safe

import os
import os.path
from threading import Thread
from traceback import format_exception
from PIL import Image

LOG = Log.add
# transparent color
TRANSPARENT = 'transparent'
# to keep all created widgets
tk_widgets = Keeper()
le_font = None

def set_rce():
    def rce(self, *args):
        # redirect tkinter error print
        err = format_exception(*args)
        LOG(err)
        print(''.join(err))
    ctk.CTk.report_callback_exception = rce

def dnd_return_handle(data):
    if '{' not in data:
        return data.split(' ')
    return [path.rstrip('}').rstrip(' ').lstrip(' ') for path in data.replace('} {', '}{').split('{')]

def set_theme(theme):
    if theme == 'system': # junk part
        theme = 'blue'
        setting.set('theme', 'blue')
        setting.save()
    if theme not in ('blue', 'dark-blue', 'green'):
        theme = f'./resources/themes/{theme}.json'
    ctk.set_default_color_theme(theme)

def set_style(style):
    if tk_widgets.main_tk == None:
        print('No main tk app?')
        return
    if style == 'system':
        return
    pywinstyles.apply_style(tk_widgets.main_tk, style)


def create_main_app_and_frames():
    class CTkDnD(ctk.CTk, tkdnd.TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.TkdndVersion = tkdnd.TkinterDnD._require(self)
    
    # create main app
    tk_widgets.main_tk = CTkDnD()
    tk_widgets.main_tk.geometry('1080x660+30+30')
    tk_widgets.main_tk.title('LtMAO')
    if os.path.exists(winLT.icon_file):
        tk_widgets.main_tk.iconbitmap(winLT.icon_file)
    global le_font
    le_font=ctk.CTkFont(family='Consolas', size=14)
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
    tk_widgets.mainleft_frame = ctk.CTkScrollableFrame(
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


def create_CSLMAO_page():
    # create page frame
    tk_widgets.CSLMAO.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.CSLMAO.page_frame.columnconfigure(0, weight=1)
    tk_widgets.CSLMAO.page_frame.rowconfigure(0, weight=1)
    tk_widgets.CSLMAO.page_frame.rowconfigure(1, weight=1)
    tk_widgets.CSLMAO.page_frame.rowconfigure(2, weight=699)
    # handle drop in cslmao
    def page_drop_cmd(event):
        if block_on_overlay():
            return
        fantome_paths = []
        paths = dnd_return_handle(event.data)
        for path in paths:
            if os.path.isfile(path):
                if path.endswith('.fantome') or path.endswith('.zip'):
                    fantome_paths.append(path)
        import_mod(fantome_paths)
    tk_widgets.CSLMAO.page_frame.drop_target_register(
        tkdnd.DND_FILES)
    tk_widgets.CSLMAO.page_frame.dnd_bind(
        '<<Drop>>', page_drop_cmd)
    # init stuffs
    tk_widgets.CSLMAO.mods = []
    tk_widgets.CSLMAO.make_overlay = None
    tk_widgets.CSLMAO.run_overlay = None
    tk_widgets.CSLMAO.toggle_all = True

    # create setting frame
    tk_widgets.CSLMAO.setting_frame = ctk.CTkFrame(
        tk_widgets.CSLMAO.page_frame, fg_color=TRANSPARENT)
    tk_widgets.CSLMAO.setting_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.CSLMAO.setting_frame.columnconfigure(0, weight=1)
    tk_widgets.CSLMAO.setting_frame.columnconfigure(1, weight=699)
    tk_widgets.CSLMAO.setting_frame.columnconfigure(2, weight=1)
    tk_widgets.CSLMAO.setting_frame.columnconfigure(3, weight=1)
    tk_widgets.CSLMAO.setting_frame.columnconfigure(4, weight=1)

    # create game folder setting
    def gamedir_cmd():
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select League of Legends/Game Folder',
            initialdir=setting.get('default_folder', None)
        )
        if dir_path != '':
            dir_path = dir_path.replace('\\', '/')
            if not os.path.exists(os.path.join(dir_path, 'League of Legends.exe')):
                raise Exception(
                    f'cslmao: Failed: Select League of Legends/Game: No "League of Legends.exe" found in {dir_path}')
            setting.set('game_folder', dir_path)
            setting.save()
            tk_widgets.CSLMAO.gamedir_value_label.configure(text=dir_path)
    tk_widgets.CSLMAO.gamedir_button = ctk.CTkButton(
        tk_widgets.CSLMAO.setting_frame,
        text='Browse Game Folder',
        image=EmojiImage.create('🎮'),
        command=gamedir_cmd,
        font=le_font
    )
    tk_widgets.CSLMAO.gamedir_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.CSLMAO.gamedir_value_label = ctk.CTkLabel(
        tk_widgets.CSLMAO.setting_frame,
        text=setting.get(
            'game_folder', 'Please choose League of Legends/Game folder.'),
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.CSLMAO.gamedir_value_label.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # extra game modes
    tk_widgets.CSLMAO.egm_label = ctk.CTkLabel(
        tk_widgets.CSLMAO.setting_frame,
        text='Extra Game Modes:',
        image=EmojiImage.create('🕹️', weird=True),
        compound=tk.LEFT,
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.CSLMAO.egm_label.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

    def egm_cmd():
        setting.set('Cslmao.extra_game_modes',
                    tk_widgets.CSLMAO.egm_checkbox.get())
        setting.save()
    tk_widgets.CSLMAO.egm_checkbox = ctk.CTkCheckBox(
        tk_widgets.CSLMAO.setting_frame,
        text='',
        command=egm_cmd,
        width=30
    )
    if setting.get('Cslmao.extra_game_modes', 0) == 1:
        tk_widgets.CSLMAO.egm_checkbox.select()
    else:
        tk_widgets.CSLMAO.egm_checkbox.deselect()
    tk_widgets.CSLMAO.egm_checkbox.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)
    
    # create cslol diagnose
    def diagnose_cmd():
        cslmao.diagnose()
    tk_widgets.CSLMAO.diagnose_button = ctk.CTkButton(
        tk_widgets.CSLMAO.setting_frame,
        text='Diagnose',
        image=EmojiImage.create('🩺'),
        command=diagnose_cmd,
        font=le_font
    )
    tk_widgets.CSLMAO.diagnose_button.grid(
        row=0, column=4, padx=5, pady=5, sticky=tk.NSEW)
    
    
    # create action frame
    tk_widgets.CSLMAO.action_frame = ctk.CTkFrame(
        tk_widgets.CSLMAO.page_frame, fg_color=TRANSPARENT)
    tk_widgets.CSLMAO.action_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.CSLMAO.action_frame.rowconfigure(0, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(0, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(1, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(2, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(3, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(4, weight=699)
    tk_widgets.CSLMAO.action_frame.columnconfigure(5, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(6, weight=1)

    # check if running overlay func
    def block_on_overlay():
        if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
            return True
        return False

    def run_cmd():
        if cslmao.preparing:
            LOG('cslmao: Error: Loading mods, can not run yet.')
            return
        if tk_widgets.CSLMAO.make_overlay == None and tk_widgets.CSLMAO.run_overlay == None:
            def run_thrd():
                profile = setting.get('Cslmao.profile', 'all')
                tk_widgets.CSLMAO.make_overlay = p = cslmao.make_overlay(
                    profile)
                cslmao.block_and_stream_process_output(
                    p, 'CSLMAO: ')
                if p.returncode == 0:
                    tk_widgets.CSLMAO.make_overlay = None
                    tk_widgets.CSLMAO.run_overlay = p2 = cslmao.run_overlay(
                        profile)
                    cslmao.block_and_stream_process_output(
                        p2, 'CSLMAO: ')
                    if p2.returncode not in (None, 0, 1):
                        tk_widgets.CSLMAO.run_button.configure(
                            text='Run',
                            image=EmojiImage.create('▶️', weird=True)
                        )
                        for stuffs in tk_widgets.CSLMAO.mods:
                            stuffs[1].configure(
                                state=tk.NORMAL
                            )
                        LOG('cslmao: Error: Run overlay failed, click this message to see full error log.')
                        tk_widgets.CSLMAO.run_overlay = None
                else:
                    tk_widgets.CSLMAO.run_button.configure(
                        text='Run',
                        image=EmojiImage.create('▶️', weird=True)
                    )
                    for stuffs in tk_widgets.CSLMAO.mods:
                        stuffs[1].configure(
                            state=tk.NORMAL
                        )
                    LOG('cslmao: Error: Make overlay failed, click this message to see full error log.')
                    tk_widgets.CSLMAO.make_overlay = None
            tk_widgets.CSLMAO.run_button.configure(
                text='Stop',
                image=EmojiImage.create('⏹️', weird=True)
            )
            for stuffs in tk_widgets.CSLMAO.mods:
                stuffs[1].configure(
                    state=tk.DISABLED
                )
            Thread(target=run_thrd, daemon=True).start()
        else:
            if tk_widgets.CSLMAO.make_overlay != None:
                tk_widgets.CSLMAO.make_overlay.kill()
            if tk_widgets.CSLMAO.run_overlay != None:
                tk_widgets.CSLMAO.run_overlay.kill()
            tk_widgets.CSLMAO.run_button.configure(
                text='Run',
                image=EmojiImage.create('▶️', weird=True)
            )
            for stuffs in tk_widgets.CSLMAO.mods:
                stuffs[1].configure(
                    state=tk.NORMAL
                )
            LOG('cslmao: Status: Stopped running overlay, idling.')
            tk_widgets.CSLMAO.make_overlay = None
            tk_widgets.CSLMAO.run_overlay = None
        tk_widgets.CSLMAO.run_button.configure(state='disabled')
        tk_widgets.CSLMAO.run_button.after(
            1000, lambda: tk_widgets.CSLMAO.run_button.configure(state='active'))
    # create run button
    tk_widgets.CSLMAO.run_button = ctk.CTkButton(
        tk_widgets.CSLMAO.action_frame,
        text='Run',
        image=EmojiImage.create('🚀'),
        command=run_cmd,
        font=le_font
    )
    tk_widgets.CSLMAO.run_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    # import func
    def import_mod(fantome_paths):
        mgs = []
        for fantome_path in fantome_paths:
            mod_path = '.'.join(os.path.basename(fantome_path).split('.')[:-1])
            mod_profile = get_mod_profile()
            if mod_profile == 'all':
                mod_profile = '0'
            mod = cslmao.create_mod(
                path=mod_path, enable=False, profile=mod_profile)
            p = cslmao.import_fantome(fantome_path, mod.get_path())
            if p.returncode == 0:
                LOG(f'cslmao: Imported: {fantome_path}')
                info, image = cslmao.get_info(mod)
                mgs.append(
                    add_mod(
                        image=image,
                        name=info['Name'],
                        author=info['Author'],
                        version=info['Version'],
                        description=info['Description'],
                        enable=mod.enable,
                        profile=mod.profile
                    )
                )
            else:
                cslmao.delete_mod(mod)
        # grid after finish import
        for mg in mgs:
            mg()
        cslmao.save_mods()  # save outside loop

    def import_cmd():
        if block_on_overlay():
            return
        fantome_paths = tkfd.askopenfilenames(
            title='Import FANTOME',
            parent=tk_widgets.main_tk,
            filetypes=(('FANTOME/ZIP file', ('*.fantome', '*.zip')),),
            initialdir=setting.get('default_folder', None)
        )
        import_mod(fantome_paths)
    # create import button
    tk_widgets.CSLMAO.import_button = ctk.CTkButton(
        tk_widgets.CSLMAO.action_frame,
        text='Import',
        image=EmojiImage.create('📥'),
        command=import_cmd,
        font=le_font
    )
    tk_widgets.CSLMAO.import_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def new_cmd():
        if block_on_overlay():
            return
        mod_path = 'New Mod'
        mod_info = {
            'Name': 'New Mod',
            'Author': 'Author',
            'Version': '1.0',
            'Description': ''
        }
        mod_profile = get_mod_profile()
        if mod_profile == 'all':
            mod_profile = '0'
        mod = cslmao.create_mod(path=mod_path, enable=False,
                                profile=mod_profile)
        cslmao.create_mod_folder(mod)
        cslmao.set_info(
            mod,
            info=mod_info,
            image_path=None
        )
        add_mod(
            image=cslmao.CSLMAO.blank_image,
            name=mod_info['Name'],
            author=mod_info['Author'],
            version=mod_info['Version'],
            description=mod_info['Description'],
            enable=mod.enable,
            profile=mod.profile
        )()
        cslmao.save_mods()
    # create new button
    tk_widgets.CSLMAO.new_button = ctk.CTkButton(
        tk_widgets.CSLMAO.action_frame,
        text='New',
        image=EmojiImage.create('💥'),
        command=new_cmd,
        font=le_font
    )
    tk_widgets.CSLMAO.new_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

    def toggle_cmd():
        need_save = False
        mod_profile = get_mod_profile()
        for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
            mod = cslmao.CSLMAO.MODS[mod_id]
            if mod_profile == 'all' or mod.profile == mod_profile:
                mod_enable = tk_widgets.CSLMAO.mods[mod_id][4]
                if tk_widgets.CSLMAO.toggle_all:
                    mod_enable.select()
                else:
                    mod_enable.deselect()
                mod.enable = tk_widgets.CSLMAO.toggle_all
                need_save = True
        if need_save:
            cslmao.save_mods()
            tk_widgets.CSLMAO.toggle_all = not tk_widgets.CSLMAO.toggle_all
    # create toggle button
    tk_widgets.CSLMAO.toggle_button = ctk.CTkButton(
        tk_widgets.CSLMAO.action_frame,
        text='On/Off All',
        image=EmojiImage.create('✅'),
        command=toggle_cmd,
        font=le_font
    )
    tk_widgets.CSLMAO.toggle_button.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)

    # create profile label
    tk_widgets.CSLMAO.profile_label = ctk.CTkLabel(
        tk_widgets.CSLMAO.action_frame,
        text='Profile: ',
        font=le_font
    )
    tk_widgets.CSLMAO.profile_label.grid(
        row=0, column=5, padx=5, pady=5, sticky=tk.NSEW)

    def profile_cmd(choice):
        refresh_profile(choice)
        setting.set('Cslmao.profile', choice)
        setting.save()
    # create profile opt
    tk_widgets.CSLMAO.profile_opt = ctk.CTkOptionMenu(
        tk_widgets.CSLMAO.action_frame,
        values=[
            'all',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9'
        ],
        command=profile_cmd,
        font=le_font
    )
    tk_widgets.CSLMAO.profile_opt.set(setting.get('Cslmao.profile', 'all'))
    tk_widgets.CSLMAO.profile_opt.grid(
        row=0, column=6, padx=5, pady=5, sticky=tk.NSEW)
    # profile funcs

    def get_mod_profile():
        return setting.get('Cslmao.profile', 'all')

    def refresh_profile(profile):
        if profile == 'all':
            for id in range(len(tk_widgets.CSLMAO.mods)):
                tk_widgets.CSLMAO.mods[id][0].grid(
                    row=id, column=0, padx=2, pady=2, sticky=tk.NSEW)
        else:
            for id in range(len(tk_widgets.CSLMAO.mods)):
                if cslmao.CSLMAO.MODS[id].profile == profile:
                    tk_widgets.CSLMAO.mods[id][0].grid(
                        row=id, column=0, padx=2, pady=2, sticky=tk.NSEW)
                else:
                    tk_widgets.CSLMAO.mods[id][0].grid_forget()
    cslmao.tk_refresh_profile=refresh_profile
    # create modlist frame
    tk_widgets.CSLMAO.modlist_frame = ctk.CTkScrollableFrame(
        tk_widgets.CSLMAO.page_frame)
    tk_widgets.CSLMAO.modlist_frame.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.CSLMAO.modlist_frame.rowconfigure(0, weight=1)
    tk_widgets.CSLMAO.modlist_frame.columnconfigure(0, weight=1)

    # link tk add mod for cslmao
    def add_mod(image, name, author, version, description, enable, profile):
        if image == None:
            image = cslmao.CSLMAO.blank_image
        id = len(tk_widgets.CSLMAO.mods)
        # create mod frame
        mod_frame = ctk.CTkFrame(
            tk_widgets.CSLMAO.modlist_frame
        )
        mod_frame.rowconfigure(0, weight=1)
        mod_frame.rowconfigure(1, weight=1)
        mod_frame.columnconfigure(0, weight=1)
        # create head frame
        head_frame = ctk.CTkFrame(
            mod_frame,
        )
        head_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.NSEW)
        head_frame.rowconfigure(0, weight=1)
        head_frame.columnconfigure(0, weight=0)
        head_frame.columnconfigure(1, weight=1)
        head_frame.columnconfigure(2, weight=10)
        head_frame.columnconfigure(4, weight=1)

        def enable_cmd(widget):
            if block_on_overlay():
                return
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[1]:
                    break
            mod_enable = tk_widgets.CSLMAO.mods[mod_id][4]
            cslmao.CSLMAO.MODS[mod_id].enable = mod_enable.get()
            cslmao.save_mods()

        # create mod label
        mod_enable = ctk.CTkCheckBox(
            head_frame,
            text='',
            width=15,
            command=lambda: enable_cmd(mod_enable)
        )
        mod_enable.grid(row=id, column=0, sticky=tk.NSEW)
        if enable:
            mod_enable.select()
        else:
            mod_enable.deselect()
        # create mod image
        mod_image = ctk.CTkLabel(
            head_frame,
            text='',
            image=ctk.CTkImage(image, size=(144, 81)),
        )
        mod_image.grid(row=id, column=1, sticky=tk.NSEW)
        # create mod info
        mod_info = ctk.CTkLabel(
            head_frame,
            text=f'[Profile {profile}] {name} by {author} V{version}\n{description}',
            font=le_font
        )
        mod_info.grid(row=id, column=2, padx=5, sticky=tk.NSEW)
        # create mod action frame
        mod_action_frame = ctk.CTkFrame(
            head_frame,
            fg_color=TRANSPARENT
        )
        mod_action_frame.grid(row=id, column=4, sticky=tk.NSEW)
        mod_action_frame.rowconfigure(0, weight=1)
        mod_action_frame.rowconfigure(1, weight=0)
        mod_action_frame.rowconfigure(2, weight=1)
        mod_action_frame.columnconfigure(0, weight=0)
        mod_action_frame.columnconfigure(1, weight=0)
        mod_action_frame.columnconfigure(2, weight=0)
        mod_action_frame.columnconfigure(3, weight=0)

        def locate_cmd(widget):
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[5]:
                    break
            os.startfile(os.path.join(
                cslmao.CSLMAO.raw_dir,
                cslmao.CSLMAO.MODS[mod_id].get_path()
            ))
        # create locate button
        locate_button = ctk.CTkButton(
            mod_action_frame,
            width=30,
            text='',
            image=EmojiImage.create('📂'),
            command=lambda: locate_cmd(locate_button)
        )
        locate_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        def edit_cmd(widget):
            if block_on_overlay():
                return
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[6]:
                    break
            expand = tk_widgets.CSLMAO.mods[mod_id][3]
            expand = not expand
            tk_widgets.CSLMAO.mods[mod_id][3] = expand
            edit_frame = tk_widgets.CSLMAO.mods[mod_id][2]
            if expand:
                edit_frame.grid(row=1, column=0, sticky=tk.NSEW)
            else:
                edit_frame.grid_forget()

        edit_button = ctk.CTkButton(
            mod_action_frame,
            width=30,
            text='',
            image=EmojiImage.create('🖊️', weird=True),
            command=lambda: edit_cmd(edit_button)
        )
        edit_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

        def export_cmd(widget):
            if block_on_overlay():
                return
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[7]:
                    break
            mod = cslmao.CSLMAO.MODS[mod_id]
            info, image = cslmao.get_info(mod)
            fantome_path = tkfd.asksaveasfilename(
                title='Export FANTOME',
                parent=tk_widgets.main_tk,
                initialfile=f'{info["Name"]} V{info["Version"]} by {info["Author"]}',
                filetypes=(('FANTOME file', '*.fantome'),),
                defaultextension='.fantome',
                initialdir=setting.get('default_folder', None)
            )
            if fantome_path != '':
                def export_thrd():
                    p = cslmao.export_fantome(
                        mod_path=os.path.join(
                            cslmao.CSLMAO.raw_dir,
                            cslmao.CSLMAO.MODS[mod_id].get_path()
                        ),
                        fantome_path=fantome_path
                    )
                    if p.returncode == 0:
                        LOG(f'cslmao: Exported: {fantome_path}')
                Thread(target=export_thrd, daemon=True).start()
        # create export button
        export_button = ctk.CTkButton(
            mod_action_frame,
            width=30,
            text='',
            image=EmojiImage.create('📤'),
            command=lambda: export_cmd(export_button)
        )
        export_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.NSEW)

        def remove_cmd(widget):
            if block_on_overlay():
                return
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[8]:
                    break
            tk_widgets.CSLMAO.mods.pop(mod_id)[0].destroy()
            cslmao.delete_mod(cslmao.CSLMAO.MODS[mod_id])
            cslmao.save_mods()

        # create remove button
        remove_button = ctk.CTkButton(
            mod_action_frame,
            width=30,
            text='',
            image=EmojiImage.create('❌'),
            command=lambda: remove_cmd(remove_button)
        )
        remove_button.grid(row=1, column=3, padx=5, pady=5, sticky=tk.NSEW)
        # create edit frame
        edit_frame = ctk.CTkFrame(
            mod_frame,
        )
        edit_frame.rowconfigure(0, weight=1)
        edit_frame.columnconfigure(0, weight=699)
        edit_frame.columnconfigure(1, weight=1)
        edit_frame.columnconfigure(2, weight=1)
        edit_left_frame = ctk.CTkFrame(
            edit_frame
        )
        edit_left_frame.grid(row=0, column=0, sticky=tk.NSEW)
        edit_left_frame.rowconfigure(0, weight=1)
        edit_left_frame.rowconfigure(1, weight=1)
        edit_left_frame.rowconfigure(2, weight=1)
        edit_left_frame.rowconfigure(3, weight=1)
        edit_left_frame.columnconfigure(0, weight=1)
        # create name entry
        name_entry = ctk.CTkEntry(
            edit_left_frame,
            font=le_font
        )
        name_entry.insert(0, name)
        name_entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        # create author entry
        author_entry = ctk.CTkEntry(
            edit_left_frame,
            font=le_font
        )
        author_entry.insert(0, author)
        author_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        # create version entry
        version_entry = ctk.CTkEntry(
            edit_left_frame,
            font=le_font
        )
        version_entry.insert(0, version)
        version_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
        # create description entry
        description_entry = ctk.CTkEntry(
            edit_left_frame,
            font=le_font
        )
        description_entry.insert(0, description)
        description_entry.grid(row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)
        edit_right_frame = ctk.CTkFrame(
            edit_frame
        )
        edit_right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        def edit_image_cmd(widget):
            if block_on_overlay():
                return
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[11]:
                    break
            png_path = tkfd.askopenfilename(
                title='Select PNG',
                parent=tk_widgets.main_tk,
                filetypes=(
                    ('PNG files', '*.png'),
                ),
                initialdir=setting.get('default_folder', None)
            )
            if png_path != '':
                tk_widgets.CSLMAO.mods[mod_id][10] = png_path
                edit_image.configure(
                    image=ctk.CTkImage(Image.open(png_path), size=(256, 144))
                )
            else:
                tk_widgets.CSLMAO.mods[mod_id][10] = None
        # create edit image
        edit_image = ctk.CTkLabel(
            edit_right_frame,
            text='',
            image=ctk.CTkImage(image, size=(256, 144))
        )
        edit_image.bind('<Button-1>', lambda event: edit_image_cmd(edit_image))
        edit_image.grid(row=0, column=0, sticky=tk.NSEW)
        edit_action_frame = ctk.CTkFrame(
            edit_frame
        )
        edit_action_frame.grid(row=0, column=2, sticky=tk.NSEW)
        edit_action_frame.rowconfigure(0, weight=1)
        edit_action_frame.rowconfigure(1, weight=0)
        edit_action_frame.rowconfigure(2, weight=0)
        edit_action_frame.rowconfigure(3, weight=0)
        edit_action_frame.rowconfigure(4, weight=1)
        edit_action_frame.columnconfigure(0, weight=1)
        edit_action_frame.columnconfigure(1, weight=0)
        edit_action_frame.columnconfigure(2, weight=1)

        # create profile opt
        edit_profile_opt = ctk.CTkOptionMenu(
            edit_action_frame,
            values=[
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8',
                '9'
            ],
            font=le_font
        )
        edit_profile_opt.set(profile)
        edit_profile_opt.grid(
            row=1, column=1, padx=20, pady=5, sticky=tk.NSEW)

        def reset_cmd(widget):
            if block_on_overlay():
                return
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[14]:
                    break
            mod = cslmao.CSLMAO.MODS[mod_id]
            info, image = cslmao.get_info(mod)
            tk_widgets.CSLMAO.mods[mod_id][15].delete(0, tk.END)
            tk_widgets.CSLMAO.mods[mod_id][16].delete(0, tk.END)
            tk_widgets.CSLMAO.mods[mod_id][17].delete(0, tk.END)
            tk_widgets.CSLMAO.mods[mod_id][18].delete(0, tk.END)
            tk_widgets.CSLMAO.mods[mod_id][15].insert(0, info['Name'])
            tk_widgets.CSLMAO.mods[mod_id][16].insert(0, info['Author'])
            tk_widgets.CSLMAO.mods[mod_id][17].insert(0, info['Version'])
            tk_widgets.CSLMAO.mods[mod_id][18].insert(0, info['Description'])
            tk_widgets.CSLMAO.mods[mod_id][10] = None
            tk_widgets.CSLMAO.mods[mod_id][11].configure(
                image=ctk.CTkImage(image, size=(256, 144))
            )
            tk_widgets.CSLMAO.mods[mod_id][19].set(mod.profile)
        # reset button
        reset_button = ctk.CTkButton(
            edit_action_frame,
            text='Reset',
            image=EmojiImage.create('🔃'),
            command=lambda: reset_cmd(reset_button),
            font=le_font
        )
        reset_button.grid(row=2, column=1, padx=20, pady=5, sticky=tk.NSEW)

        def save_cmd(widget):
            if block_on_overlay():
                return
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[9]:
                    break
            info = {
                'Name': name_entry.get(),
                'Author': author_entry.get(),
                'Version': version_entry.get(),
                'Description': description_entry.get()
            }
            mod = cslmao.CSLMAO.MODS[mod_id]
            image = tk_widgets.CSLMAO.mods[mod_id][10]
            cslmao.set_info(mod, info, image)
            if image != None:
                tk_widgets.CSLMAO.mods[mod_id][13].configure(
                    image=ctk.CTkImage(Image.open(image), size=(144, 81))
                )
            mod.profile = tk_widgets.CSLMAO.mods[mod_id][19].get()
            tk_widgets.CSLMAO.mods[mod_id][12].configure(
                text=f'[Profile {mod.profile}] {info["Name"]} by {info["Author"]} V{info["Version"]}\n{info["Description"]}'
            )
            cslmao.CSLMAO.save_mods()
            refresh_profile(
                setting.get('Cslmao.profile', 'all'))
        # create save button
        save_button = ctk.CTkButton(
            edit_action_frame,
            text='Save',
            image=EmojiImage.create('💾'),
            command=lambda: save_cmd(save_button),
            font=le_font
        )
        save_button.grid(row=3, column=1, padx=20, pady=5, sticky=tk.NSEW)
        tk_widgets.CSLMAO.mods.append([
            mod_frame,
            mod_enable,
            edit_frame,
            False,  # expand edit frame
            mod_enable,
            locate_button,
            edit_button,
            export_button,
            remove_button,
            save_button,
            None,  # edit image path
            edit_image,
            mod_info,
            mod_image,
            reset_button,
            name_entry,
            author_entry,
            version_entry,
            description_entry,
            edit_profile_opt
        ])
        # return out as a grid method of this mod_frame
        # so we can control when to grid it later
        return lambda id=id: mod_frame.grid(row=id, column=0, padx=2, pady=2, sticky=tk.NSEW)
    cslmao.tk_add_mod = add_mod


def create_LFI_page():
    # create page frame
    tk_widgets.LFI.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.LFI.page_frame.columnconfigure(0, weight=1)
    tk_widgets.LFI.page_frame.rowconfigure(0, weight=1)
    tk_widgets.LFI.page_frame.rowconfigure(1, weight=699)
    # handle drop in LFI
    def page_drop_cmd(event):
        def page_drop_thrd():
            paths = dnd_return_handle(event.data)
            for path in paths:
                path = path.replace('\\', '/')
                if os.path.isdir(path):
                    folderread_lfi(path)
                else:
                    fileread_lfi(path)

        if check_thread_safe(tk_widgets.LFI.reading_thread):
            tk_widgets.LFI.reading_thread = Thread(
                    target=page_drop_thrd,
                    daemon=True
                )
            tk_widgets.LFI.reading_thread.start()
        else:
            LOG('leaguefile_inspector: Failed: A thread is already running, wait for it to finished.')
    tk_widgets.LFI.page_frame.drop_target_register(tkdnd.DND_FILES)
    tk_widgets.LFI.page_frame.dnd_bind('<<Drop>>', page_drop_cmd)
    # init stuffs
    tk_widgets.LFI.reading_thread = None
    tk_widgets.LFI.loaded_files = []
    tk_widgets.LFI.use_ritobin = True
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
    tk_widgets.LFI.input_frame.columnconfigure(3, weight=1)
    tk_widgets.LFI.input_frame.columnconfigure(4, weight=699)
    # create view frame
    tk_widgets.LFI.view_frame = ctk.CTkScrollableFrame(
        tk_widgets.LFI.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.LFI.view_frame.grid(
        row=1, column=0, padx=0, pady=0, sticky=tk.NSEW)
    tk_widgets.LFI.view_frame.columnconfigure(0, weight=1)
    tk_widgets.LFI.view_frame._parent_canvas.unbind_all('<MouseWheel>')
    
    def read_file(file_path, hastables=None):
        # read one file function
        if file_path.endswith('.bin') and tk_widgets.LFI.use_ritobin:
            path, fsize, ftype, json = leaguefile_inspector.read_ritobin(
                file_path)
        else:
            path, fsize, ftype, json = leaguefile_inspector.read_lfi(
                file_path, hastables)
        if json == None:
            return lambda: None
        # id of this file
        file_frame_id = len(tk_widgets.LFI.loaded_files)
        # create file frame
        file_frame = ctk.CTkFrame(
            tk_widgets.LFI.view_frame
        )
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
            search_entry = tk_widgets.LFI.loaded_files[file_frame_id][7]
            toggle = not toggle
            if toggle:
                content_frame.grid(row=1, column=0,
                                   padx=0, pady=0, sticky=tk.NSEW)
                search_entry.grid(row=0, column=2, padx=0,
                                  pady=0, sticky=tk.E)
            else:
                content_frame.grid_forget()
                search_entry.grid_forget()
            tk_widgets.LFI.loaded_files[file_frame_id][2] = toggle
        # create view button
        view_button = ctk.CTkButton(
            head_frame,
            width=30,
            text='',
            image=EmojiImage.create('🔽'),
            fg_color=TRANSPARENT,
            command=lambda: view_cmd(file_frame_id)
        )
        view_button.grid(row=0, column=0, padx=2,
                         pady=2, sticky=tk.W)
        # create file label
        file_label = ctk.CTkLabel(
            head_frame,
            text=f'[{fsize}] [{ftype.upper()}] {path}',
            anchor=tk.W,
            justify=tk.LEFT,
            font=le_font
        )
        file_label.grid(row=0, column=1, padx=2,
                        pady=2, sticky=tk.W)
        
        # create search entry
        search_entry = ctk.CTkEntry(
            head_frame,
            placeholder_text='Search',
            width=300,
            font=le_font
        )

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
                'search', foreground=tk_widgets.c_active_fg[0])
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
            width=30,
            text='',
            image=EmojiImage.create('❌'),
            fg_color=TRANSPARENT,
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
            content_frame,
            font=le_font
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
                False,  # deleted or not
                search_entry
            ]
        )
        return lambda id=file_frame_id: file_frame.grid(row=id, column=0, padx=2, pady=5, sticky=tk.NSEW)
    
    def fileread_lfi(file_paths):
        hash_manager.read_all_hashes()
        fgs = [read_file(file_path, hash_manager.HASHTABLES) for file_path in file_paths]
        hash_manager.free_all_hashes()
        for fg in fgs:
            fg()
        

    def fileread_cmd():
        if check_thread_safe(tk_widgets.LFI.reading_thread):
            file_paths = tkfd.askopenfilenames(
                parent=tk_widgets.main_tk,
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
                            '*.tex',
                            '*.mapgeo',
                            '*.bnk',
                            '*.wpk',
                            '*.wad.client'
                        )
                     ),
                    ('All files', '*.*'),
                ),
                initialdir=setting.get('default_folder', None)
            )
            if len(file_paths) > 0:
                def fileread_thrd():
                    fileread_lfi(file_paths)
                tk_widgets.LFI.reading_thread = Thread(
                    target=fileread_thrd,
                    daemon=True
                )
                tk_widgets.LFI.reading_thread.start()
        else:
            LOG(
                'leaguefile_inspector: Failed: A thread is already running, wait for it to finished.')
    # create file read button
    tk_widgets.LFI.fileread_button = ctk.CTkButton(
        tk_widgets.LFI.input_frame,
        text='Read Files',
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=fileread_cmd,
        font=le_font
    )
    tk_widgets.LFI.fileread_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def folderread_lfi(dir_path):
        fgs = []
        hash_manager.read_all_hashes()
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(
                    root, file).replace('\\', '/')
                fgs.append(read_file(
                    file_path, hash_manager.HASHTABLES))
        hash_manager.free_all_hashes()
        for fg in fgs:
            fg()

    def folderread_cmd():
        if check_thread_safe(tk_widgets.LFI.reading_thread):
            dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Folder To Read',
                initialdir=setting.get('default_folder', None)
            )
            if dir_path != '':
                def folderread_thrd():
                    folderread_lfi(dir_path)
                tk_widgets.LFI.reading_thread = Thread(
                    target=folderread_thrd,
                    daemon=True
                )
                tk_widgets.LFI.reading_thread.start()
        else:
            LOG(
                'leaguefile_inspector: Failed: A thread is already running, wait for it to finished.')
    # create folder read button
    tk_widgets.LFI.folderread_button = ctk.CTkButton(
        tk_widgets.LFI.input_frame,
        text='Read Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=folderread_cmd,
        font=le_font
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
        LOG(f'leaguefile_inspector: Done: Cleared all loaded files.')
    # create clear button
    tk_widgets.LFI.clear_button = ctk.CTkButton(
        tk_widgets.LFI.input_frame,
        text='Clear',
        image=EmojiImage.create('❌'),
        anchor=tk.CENTER,
        command=clear_cmd,
        font=le_font
    )
    tk_widgets.LFI.clear_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

    def ritobin_cmd():
        tk_widgets.LFI.use_ritobin = tk_widgets.LFI.use_ritobin_switch.get() == 1
        setting.set('LFI.use_ritobin',
                    tk_widgets.LFI.use_ritobin)
        setting.save()
    # create use ritobin switch
    tk_widgets.LFI.use_ritobin_switch = ctk.CTkSwitch(
        tk_widgets.LFI.input_frame,
        text='Read BIN files using ritobin',
        command=ritobin_cmd,
        font=le_font
    )
    tk_widgets.LFI.use_ritobin = setting.get(
        'LFI.use_ritobin', False)
    if tk_widgets.LFI.use_ritobin:
        tk_widgets.LFI.use_ritobin_switch.select()
    else:
        tk_widgets.LFI.use_ritobin_switch.deselect()
    tk_widgets.LFI.use_ritobin_switch.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)


def create_AMV_page():
    tk_widgets.AMV.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.AMV.page_frame.columnconfigure(0, weight=1)
    tk_widgets.AMV.page_frame.rowconfigure(0, weight=1)
    tk_widgets.AMV.page_frame.rowconfigure(1, weight=1)
    tk_widgets.AMV.page_frame.rowconfigure(2, weight=699)
    # handle drop in AMV
    def page_drop_cmd(event):
        paths = dnd_return_handle(event.data)
        for path in paths:
            path = path.replace('\\', '/')
            if os.path.isfile(path):
                if path.endswith('.skl'):
                    tk_widgets.AMV.skl_entry.delete(0, tk.END)
                    tk_widgets.AMV.skl_entry.insert(tk.END, path)
                elif path.endswith('.bin'):
                    tk_widgets.AMV.bin_entry.delete(0, tk.END)
                    tk_widgets.AMV.bin_entry.insert(tk.END, path)
    tk_widgets.AMV.page_frame.drop_target_register(tkdnd.DND_FILES)
    tk_widgets.AMV.page_frame.dnd_bind('<<Drop>>', page_drop_cmd)

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
        font=le_font
    )
    tk_widgets.AMV.skl_entry.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create skl browse button

    def sklbrowse_cmd():
        skl_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select SKL file',
            filetypes=(
                ('SKL files', '*.skl'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.AMV.skl_entry.delete(0, tk.END)
        tk_widgets.AMV.skl_entry.insert(tk.END, skl_path)
    tk_widgets.AMV.sklbrowse_button = ctk.CTkButton(
        tk_widgets.AMV.input_frame,
        text='Browse SKL',
        image=EmojiImage.create('🦴'),
        anchor=tk.CENTER,
        command=sklbrowse_cmd,
        font=le_font
    )
    tk_widgets.AMV.sklbrowse_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create bin entry
    tk_widgets.AMV.bin_entry = ctk.CTkEntry(
        tk_widgets.AMV.input_frame,
        font=le_font
    )
    tk_widgets.AMV.bin_entry.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def binbrowse_cmd():
        bin_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select Animation BIN file',
            filetypes=(
                ('BIN files', ['*.bin']),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.AMV.bin_entry.delete(0, tk.END)
        tk_widgets.AMV.bin_entry.insert(tk.END, bin_path)
    # create bin browse button
    tk_widgets.AMV.binbrowse_button = ctk.CTkButton(
        tk_widgets.AMV.input_frame,
        text='Browse Animation BIN',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=binbrowse_cmd,
        font=le_font
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
        LOG('animask_viewer: Running: Load weight table')

        joint_names = []
        mask_names = []
        weights = []
        # read skl
        skl_path = tk_widgets.AMV.skl_entry.get()
        if skl_path != '':
            skl_file = pyRitoFile.read_skl(skl_path)
            LOG(f'animask_viewer: Done: Read {skl_path}')
            joint_names = [joint.name for joint in skl_file.joints]
        # read bin
        bin_path = tk_widgets.AMV.bin_entry.get()
        if bin_path != '':
            hash_manager.read_bin_hashes()
            bin_file = pyRitoFile.read_bin(bin_path)
            bin_file.un_hash(hash_manager.HASHTABLES)
            hash_manager.free_bin_hashes()
            tk_widgets.AMV.bin_loaded = bin_file
            LOG(f'animask_viewer: Done: Read {bin_path}')
            mask_data = animask_viewer.get_weights(bin_file)
            mask_names, weights = list(
                mask_data.keys()), list(mask_data.values())

        # get table row and column length
        tk_widgets.AMV.table_row = len(joint_names)
        tk_widgets.AMV.table_column = len(mask_names)
        if tk_widgets.AMV.table_row == 0:
            raise Exception(
                'animask_viewer: Failed: Load weight table: No joints found.')

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

        def focus_cmd(event):
            top_y = event.widget.master.winfo_y()
            bot_y = top_y+event.widget.master.winfo_height()
            top_yview, bot_yview = tk_widgets.AMV.vtable_frame._parent_canvas.yview()
            height = tk_widgets.AMV.vtable_frame.winfo_height()
            top_yview, bot_yview = int(
                top_yview * height), int(bot_yview*height)
            if bot_y > bot_yview:
                d = bot_y-bot_yview
                tk_widgets.AMV.vtable_frame._parent_canvas.yview_scroll(
                    d, 'units')
            elif top_y < top_yview:
                d = top_y-top_yview
                tk_widgets.AMV.vtable_frame._parent_canvas.yview_scroll(
                    d, 'units')

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
                        text=mask_names[j-1],
                        font=le_font
                    )
                # create joint name labels
                elif j == 0:
                    tk_widgets.AMV.table_widgets[windex] = ctk.CTkLabel(
                        tk_widgets.AMV.vtable_frame,
                        width=160,
                        text=f'[{i-1}] {joint_names[i-1]}',
                        anchor=tk.W,
                        font=le_font
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
                        ),
                        font=le_font
                    )
                    tk_widgets.AMV.table_widgets[windex].bind(
                        '<FocusIn>', focus_cmd)
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
        LOG('animask_viewer: Done: Load weight table')
    tk_widgets.AMV.load_button = ctk.CTkButton(
        tk_widgets.AMV.action_frame,
        text='Load',
        image=EmojiImage.create('🗿'),
        command=load_cmd,
        font=le_font
    )
    tk_widgets.AMV.load_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    # create save button
    def save_cmd():
        if not tk_widgets.AMV.table_loaded:
            return

        # save to txt file (bin later)
        bin_path = tkfd.asksaveasfilename(
            parent=tk_widgets.main_tk,
            title='Select output Animation BIN path',
            filetypes=(
                ('BIN files', '*.bin'),
                ('All files', '*.*'),
            ),
            defaultextension='.bin',
            initialdir=setting.get('default_folder', None)
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
        LOG(f'animask_viewer: Done: Write: {bin_path}')
    tk_widgets.AMV.save_button = ctk.CTkButton(
        tk_widgets.AMV.action_frame,
        text='Save As',
        image=EmojiImage.create('💾'),
        command=save_cmd,
        font=le_font
    )
    tk_widgets.AMV.save_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create clear button
    def clear_cmd():
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
        LOG('animask_viewer: Done: Clear weight table')
    tk_widgets.AMV.clear_button = ctk.CTkButton(
        tk_widgets.AMV.action_frame,
        text='Clear',
        image=EmojiImage.create('❌'),
        command=clear_cmd,
        font=le_font
    )
    tk_widgets.AMV.clear_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)


def create_HM_page():
    tk_widgets.HM.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.HM.page_frame.columnconfigure(0, weight=1)
    tk_widgets.HM.page_frame.rowconfigure(0, weight=1)
    tk_widgets.HM.page_frame.rowconfigure(1, weight=1)
    tk_widgets.HM.page_frame.rowconfigure(2, weight=1)
    tk_widgets.HM.page_frame.rowconfigure(3, weight=699)

    tk_widgets.HM.extracting_thread = None

    # create info frame
    tk_widgets.HM.info_frame = ctk.CTkFrame(
        tk_widgets.HM.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.HM.info_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.info_frame.columnconfigure(0, weight=699)
    tk_widgets.HM.info_frame.columnconfigure(1, weight=0)
    tk_widgets.HM.info_frame.columnconfigure(2, weight=0)
    tk_widgets.HM.info_frame.columnconfigure(3, weight=0)
    tk_widgets.HM.info_frame.rowconfigure(0, weight=1)
    # create folder labels and folder buttons
    folder_label_text = [
        f'CDTB: {hash_manager.CDTBHashes.local_dir}',
        f'Extracted: {hash_manager.ExtractedHashes.local_dir}',
        f'Custom: {hash_manager.CustomHashes.local_dir}'
    ]

    def change_cmd(index, label):
        dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Folder To Extract',
                initialdir=setting.get('default_folder', None)
            )
        if dir_path != '':
            full_dir_path = os.path.abspath(dir_path)
            full_cdtb_path = os.path.abspath(hash_manager.CDTBHashes.local_dir)
            full_extracted_path = os.path.abspath(hash_manager.ExtractedHashes.local_dir)
            full_custom_path = os.path.abspath(hash_manager.CustomHashes.local_dir)
            if index == 0:
                if full_dir_path in (full_extracted_path, full_custom_path):
                    raise Exception(f'hash_manager: Failed: Change hashes path: {full_dir_path} is already selected as another hashes path. All 3 hashes paths must be different.')
                hash_manager.CDTBHashes.local_dir = dir_path
                setting.set('CDTBHashes.local_dir', dir_path)
                label.configure(text = f'CDTB: {hash_manager.CDTBHashes.local_dir}')
                setting.save()
            elif index == 1:
                if full_dir_path in (full_cdtb_path, full_custom_path):
                    raise Exception(f'hash_manager: Failed: Change hashes path: {full_dir_path} is already selected as another hashes path. All 3 hashes paths must be different.')
                hash_manager.ExtractedHashes.local_dir = dir_path
                setting.set('ExtractedHashes.local_dir', dir_path)
                label.configure(text = f'Extracted: {hash_manager.ExtractedHashes.local_dir}')
                setting.save()
            else:
                if full_dir_path in (full_cdtb_path, full_extracted_path):
                    raise Exception(f'hash_manager: Failed: Change hashes path: {full_dir_path} is already selected as another hashes path. All 3 hashes paths must be different.')
                hash_manager.CustomHashes.local_dir = dir_path
                setting.set('CustomHashes.local_dir', dir_path)
                label.configure(text = f'Custom: {hash_manager.CustomHashes.local_dir}')
                setting.save()

    def folder_cmd(index):
        if index == 0:
            os.startfile(os.path.abspath(
                hash_manager.CDTBHashes.local_dir))
        elif index == 1:
            os.startfile(os.path.abspath(
                hash_manager.ExtractedHashes.local_dir))
        else:
            os.startfile(os.path.abspath(
                hash_manager.CustomHashes.local_dir))
    # create folder buttons
    for i in range(3):
        folder_label = ctk.CTkLabel(
            tk_widgets.HM.info_frame,
            text=folder_label_text[i],
            anchor=tk.W,
            font=le_font
        )
        folder_label.grid(row=i, column=0, padx=5,
                          pady=5, sticky=tk.NSEW)
        change_button = ctk.CTkButton(
            tk_widgets.HM.info_frame,
            text='Change',
            image=EmojiImage.create('🛠️'),
            command=lambda index=i, label=folder_label: change_cmd(index, label),
            font=le_font
        )
        change_button.grid(row=i, column=1, padx=5,
                           pady=5, sticky=tk.NSEW)
        folder_button = ctk.CTkButton(
            tk_widgets.HM.info_frame,
            text='Open',
            image=EmojiImage.create('📂'),
            command=lambda index=i: folder_cmd(index),
            font=le_font
        )
        folder_button.grid(row=i, column=2, padx=5,
                           pady=5, sticky=tk.NSEW)

    def reset_cmd():
        hash_manager.reset_custom_hashes(*hash_manager.ALL_HASHES)
        LOG('hash_manager: Done: Reset Custom Hashes to CDTB Hashes.')
    # create reset button
    reset_button = ctk.CTkButton(
        tk_widgets.HM.info_frame,
        text='Reset to CDTB',
        image=EmojiImage.create('❌'),
        command=reset_cmd,
        font=le_font
    )
    reset_button.grid(row=2, column=3, padx=5, pady=5, sticky=tk.NSEW)

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

    def fileextract_cmd():
        if check_thread_safe(tk_widgets.HM.extracting_thread):
            file_paths = tkfd.askopenfilenames(
                parent=tk_widgets.main_tk,
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
                    ('All files', '*.*'),
                ),
                initialdir=setting.get('default_folder', None)
            )
            if len(file_paths) > 0:
                def working_thrd():
                    Log.tk_cooldown = 5000
                    hash_manager.ExtractedHashes.extract(*file_paths)
                    Log.tk_cooldown = 0
                    LOG('hash_manager: Done: Extract hashes.')
                tk_widgets.HM.extracting_thread = Thread(
                    target=working_thrd,
                    daemon=True
                )
                tk_widgets.HM.extracting_thread.start()
        else:
            LOG(
                'hash_manager: Failed: A thread is already running, wait for it to finished.')
    # create file read button
    tk_widgets.HM.fileread_button = ctk.CTkButton(
        tk_widgets.HM.input_frame,
        text='Extract From Files',
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=fileextract_cmd,
        font=le_font
    )
    tk_widgets.HM.fileread_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def folderextract_cmd():
        if check_thread_safe(tk_widgets.HM.extracting_thread):
            dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Folder To Extract',
                initialdir=setting.get('default_folder', None)
            )
            if dir_path != '':
                file_paths = []
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_paths.append(os.path.join(
                            root, file).replace('\\', '/'))
                if len(file_paths) > 0:
                    def working_thrd():
                        Log.tk_cooldown = 5000
                        hash_manager.ExtractedHashes.extract(*file_paths)
                        Log.tk_cooldown = 0
                        LOG('hash_manager: Done: Extract hashes.')
                    tk_widgets.HM.extracting_thread = Thread(
                        target=working_thrd,
                        daemon=True
                    )
                    tk_widgets.HM.extracting_thread.start()
        else:
            LOG(
                'hash_manager: Failed: A thread is already running, wait for it to finished.')
    # create folder read button
    tk_widgets.HM.folderread_button = ctk.CTkButton(
        tk_widgets.HM.input_frame,
        text='Extract From Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=folderextract_cmd,
        font=le_font
    )
    tk_widgets.HM.folderread_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create generate frame
    tk_widgets.HM.generate_frame = ctk.CTkFrame(
        tk_widgets.HM.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.HM.generate_frame.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.generate_frame.columnconfigure(0, weight=8)
    tk_widgets.HM.generate_frame.columnconfigure(1, weight=2)
    tk_widgets.HM.generate_frame.rowconfigure(0, weight=1)
    tk_widgets.HM.generate_frame.rowconfigure(1, weight=1)
    tk_widgets.HM.generate_frame.rowconfigure(2, weight=1)
    tk_widgets.HM.generate_frame.rowconfigure(3, weight=1)
    tk_widgets.HM.generate_frame.rowconfigure(4, weight=699)
    # create bin label
    tk_widgets.HM.bin_label = ctk.CTkLabel(
        tk_widgets.HM.generate_frame,
        text='Generate BIN hash:',
        font=le_font
    )
    tk_widgets.HM.bin_label.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create add bin frame
    tk_widgets.HM.addbin_frame = ctk.CTkFrame(
        tk_widgets.HM.generate_frame
    )
    tk_widgets.HM.addbin_frame.grid(
        row=0, column=1, padx=0, pady=0, sticky=tk.NSEW)

    def addbin_cmd(filename):
        rawlines = [
            rawline
            for rawline in tk_widgets.HM.binraw_text.get('1.0', 'end-1c').split('\n')
            if rawline != ''
        ]
        hashlines = [
            hashline
            for hashline in tk_widgets.HM.binhash_text.get('1.0', 'end-1c').split('\n')
            if hashline != ''
        ]
        if len(rawlines) > 0:
            hash_manager.CustomHashes.read_hashes(filename)
            for i in range(len(rawlines)):
                hash_manager.HASHTABLES[filename][hashlines[i]] = rawlines[i]
            hash_manager.CustomHashes.write_hashes(filename)
            hash_manager.CustomHashes.free_hashes(filename)
    # create add bin hash button
    tk_widgets.HM.addentry_button = ctk.CTkButton(
        tk_widgets.HM.addbin_frame,
        text='Entries',
        image=EmojiImage.create('👉🏻', weird=True),
        width=50,
        command=lambda: addbin_cmd('hashes.binentries.txt'),
        font=le_font
    )
    tk_widgets.HM.addentry_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.addfield_button = ctk.CTkButton(
        tk_widgets.HM.addbin_frame,
        text='Fields',
        image=EmojiImage.create('👉🏻', weird=True),
        width=50,
        command=lambda: addbin_cmd('hashes.binfields.txt'),
        font=le_font
    )
    tk_widgets.HM.addfield_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.addtype_button = ctk.CTkButton(
        tk_widgets.HM.addbin_frame,
        text='Types',
        image=EmojiImage.create('👉🏻', weird=True),
        width=50,
        command=lambda: addbin_cmd('hashes.bintypes.txt'),
        font=le_font
    )
    tk_widgets.HM.addtype_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.addhash_button = ctk.CTkButton(
        tk_widgets.HM.addbin_frame,
        text='Hashes',
        image=EmojiImage.create('👉🏻', weird=True),
        width=50,
        command=lambda: addbin_cmd('hashes.binhashes.txt'),
        font=le_font
    )
    tk_widgets.HM.addhash_button.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)

    def binraw_cmd():
        raw = tk_widgets.HM.binraw_text.get('1.0', 'end-1c')
        if raw != '':
            hashlines = [pyRitoFile.bin_hash(
                rawline) if rawline != '' else '' for rawline in raw.split('\n')]
            tk_widgets.HM.binhash_text.configure(state=tk.NORMAL)
            tk_widgets.HM.binhash_text.delete('1.0', tk.END)
            tk_widgets.HM.binhash_text.insert('1.0', '\n'.join(hashlines))
            tk_widgets.HM.binhash_text.configure(state=tk.DISABLED)
        else:
            tk_widgets.HM.binhash_text.configure(state=tk.NORMAL)
            tk_widgets.HM.binhash_text.delete('1.0', tk.END)
            tk_widgets.HM.binhash_text.configure(state=tk.DISABLED)
    # create bin raw text
    tk_widgets.HM.binraw_text = ctk.CTkTextbox(
        tk_widgets.HM.generate_frame,
        height=100,
        wrap=tk.NONE,
        font=le_font
    )
    tk_widgets.HM.binraw_text.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.binraw_text.bind('<KeyRelease>', lambda event: binraw_cmd())
    # create bin hash text
    tk_widgets.HM.binhash_text = ctk.CTkTextbox(
        tk_widgets.HM.generate_frame,
        height=100,
        wrap=tk.NONE,
        state=tk.DISABLED,
        font=le_font
    )
    tk_widgets.HM.binhash_text.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create wad label
    tk_widgets.HM.wad_label = ctk.CTkLabel(
        tk_widgets.HM.generate_frame,
        text='Generate WAD hash:',
        font=le_font
    )
    tk_widgets.HM.wad_label.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create add wad frame
    tk_widgets.HM.addwad_frame = ctk.CTkFrame(
        tk_widgets.HM.generate_frame
    )
    tk_widgets.HM.addwad_frame.grid(
        row=2, column=1, padx=0, pady=0, sticky=tk.NSEW)

    def addwad_cmd(filename):
        rawlines = [
            rawline
            for rawline in tk_widgets.HM.wadraw_text.get('1.0', 'end-1c').split('\n')
            if rawline != ''
        ]
        hashlines = [
            hashline
            for hashline in tk_widgets.HM.wadhash_text.get('1.0', 'end-1c').split('\n')
            if hashline != ''
        ]
        if len(rawlines) > 0:
            hash_manager.CustomHashes.read_hashes(filename)
            for i in range(len(rawlines)):
                hash_manager.HASHTABLES[filename][hashlines[i]] = rawlines[i]
            hash_manager.CustomHashes.write_hashes(filename)
            hash_manager.CustomHashes.free_hashes(filename)
    # create add bin hash button
    tk_widgets.HM.addgame_button = ctk.CTkButton(
        tk_widgets.HM.addwad_frame,
        text='Game',
        image=EmojiImage.create('👉🏻', weird=True),
        width=50,
        command=lambda: addwad_cmd('hashes.game.txt'),
        font=le_font
    )
    tk_widgets.HM.addgame_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.addlcu_button = ctk.CTkButton(
        tk_widgets.HM.addwad_frame,
        text='Lcu',
        image=EmojiImage.create('👉🏻', weird=True),
        width=50,
        command=lambda: addwad_cmd('hashes.lcu.txt'),
        font=le_font
    )
    tk_widgets.HM.addlcu_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def wadraw_cmd():
        raw = tk_widgets.HM.wadraw_text.get('1.0', 'end-1c')
        if raw != '':
            hashlines = [pyRitoFile.wad_hash(rawline)
                         for rawline in raw.split('\n') if rawline != '']
            tk_widgets.HM.wadhash_text.configure(state=tk.NORMAL)
            tk_widgets.HM.wadhash_text.delete('1.0', tk.END)
            tk_widgets.HM.wadhash_text.insert('1.0', '\n'.join(hashlines))
            tk_widgets.HM.wadhash_text.configure(state=tk.DISABLED)
        else:
            tk_widgets.HM.wadhash_text.configure(state=tk.NORMAL)
            tk_widgets.HM.wadhash_text.delete('1.0', tk.END)
            tk_widgets.HM.wadhash_text.configure(state=tk.DISABLED)
    # create wad raw text
    tk_widgets.HM.wadraw_text = ctk.CTkTextbox(
        tk_widgets.HM.generate_frame,
        height=100,
        wrap=tk.NONE,
        font=le_font
    )
    tk_widgets.HM.wadraw_text.grid(
        row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.wadraw_text.bind('<KeyRelease>', lambda event: wadraw_cmd())
    # create wad hash text
    tk_widgets.HM.wadhash_text = ctk.CTkTextbox(
        tk_widgets.HM.generate_frame,
        height=100,
        wrap=tk.NONE,
        state=tk.DISABLED,
        font=le_font
    )
    tk_widgets.HM.wadhash_text.grid(
        row=3, column=1, padx=5, pady=5, sticky=tk.NSEW)


def create_VH_page():
    # create page frame
    tk_widgets.VH.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.VH.page_frame.columnconfigure(0, weight=1)
    tk_widgets.VH.page_frame.rowconfigure(0, weight=1)
    tk_widgets.VH.page_frame.rowconfigure(1, weight=699)
    tk_widgets.VH.page_frame.rowconfigure(2, weight=1)
    # handle drop in VH
    def page_drop_cmd(event):
        tk_widgets.VH.scanned_fantomes = []
        paths = dnd_return_handle(event.data)
        # get all fantome paths
        fantome_paths = []
        for path in paths:
            path = path.replace('\\', '/')
            if os.path.isfile(path):
                if path.endswith('.fantome') or path.endswith('.zip'):
                    fantome_paths.append(path)
            else:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.fantome') or file.endswith('.zip'):
                            fantome_paths.append(os.path.join(root, file).replace('\\', '/'))
        # scane fantome paths
        info_text = ''
        for fantome_path in fantome_paths:
            info_text += fantome_path
            try: 
                info, image, wads = vo_helper.scan_fantome(fantome_path)
                info_text += '\n\nInfo:\n'
                info_text += ''.join(f'{key}: {info[key]}\n' for key in info)
                info_text += '\nFiles:\n'
                info_text += 'META/info.json\n'
                if image:
                    info_text += 'META/image.png\n'
                if len(wads) > 0:
                    info_text += ''.join(f'{wad_name}\n' for wad_name in wads)
                info_text += '\n\n'
                tk_widgets.VH.scanned_fantomes.append(fantome_path)
            except Exception as e:
                info_text += '\n'+str(e) + '\n\n'
        tk_widgets.VH.info_text.configure(state=tk.NORMAL)
        tk_widgets.VH.info_text.delete('1.0', tk.END)
        tk_widgets.VH.info_text.insert(tk.END, info_text)
        tk_widgets.VH.info_text.configure(state=tk.DISABLED)
        tk_widgets.VH.input_entry.delete(0, tk.END)
        tk_widgets.VH.input_entry.insert(tk.END, 'Files dropped, click remake next')

    tk_widgets.VH.page_frame.drop_target_register(tkdnd.DND_FILES)
    tk_widgets.VH.page_frame.dnd_bind('<<Drop>>', page_drop_cmd)
    # init stuffs
    tk_widgets.VH.making_thread = None
    tk_widgets.VH.scanned_fantomes = []
    # create input frame
    tk_widgets.VH.input_frame = ctk.CTkFrame(
        tk_widgets.VH.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.VH.input_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.VH.input_frame.rowconfigure(0, weight=1)
    tk_widgets.VH.input_frame.columnconfigure(0, weight=9)
    tk_widgets.VH.input_frame.columnconfigure(1, weight=1)
    tk_widgets.VH.input_frame.columnconfigure(2, weight=1)
    # create input entry
    tk_widgets.VH.input_entry = ctk.CTkEntry(
        tk_widgets.VH.input_frame,
        font=le_font
    )
    tk_widgets.VH.input_entry.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def browse_fantome_cmd():
        tk_widgets.VH.scanned_fantomes = []
        fantome_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select FANTOME/ZIP that contains VO WAD',
            filetypes=(
                ('FANTOME/ZIP files',
                    (
                        '*.fantome',
                        '*.zip',
                    )
                 ),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        if fantome_path != '':
            # update info text
            info_text = fantome_path
            try:
                info, image, wads = vo_helper.scan_fantome(fantome_path)
                info_text += '\n\nInfo:\n'
                info_text += ''.join(f'{key}: {info[key]}\n' for key in info)
                info_text += '\nFiles:\n'
                info_text += 'META/info.json\n'
                if image:
                    info_text += 'META/image.png\n'
                if len(wads) > 0:
                    info_text += ''.join(f'{wad_name}\n' for wad_name in wads)
                tk_widgets.VH.scanned_fantomes.append(fantome_path)
            except Exception as e:
                info_text += '\n'+str(e)
            tk_widgets.VH.info_text.configure(state=tk.NORMAL)
            tk_widgets.VH.info_text.delete('1.0', tk.END)
            tk_widgets.VH.info_text.insert(tk.END, info_text)
            tk_widgets.VH.info_text.configure(state=tk.DISABLED)
        else:
            tk_widgets.VH.info_text.configure(state=tk.NORMAL)
            tk_widgets.VH.info_text.delete('1.0', tk.END)
            tk_widgets.VH.info_text.configure(state=tk.DISABLED)
        tk_widgets.VH.input_entry.delete(0, tk.END)
        tk_widgets.VH.input_entry.insert(tk.END, fantome_path)
    # create browse fantome button
    tk_widgets.VH.browsefantome_button = ctk.CTkButton(
        tk_widgets.VH.input_frame,
        text='Browse FANTOME/ZIP',
        image=EmojiImage.create('🐍'),
        anchor=tk.CENTER,
        command=browse_fantome_cmd,
        font=le_font
    )
    tk_widgets.VH.browsefantome_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    
    def browsefolder_cmd():
        tk_widgets.VH.scanned_fantomes = []
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select Folder of FANTOMEs/ZIPs',
            initialdir=setting.get('default_folder', None)
        )
        if dir_path != '':
            fantome_paths = []
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('.fantome') or file.endswith('.zip'):
                        fantome_paths.append(os.path.join(root, file).replace('\\', '/'))
            info_text = ''
            for fantome_path in fantome_paths:
                info_text += fantome_path
                # update info text
                try:
                    info, image, wads = vo_helper.scan_fantome(fantome_path)
                    info_text += '\n\nInfo:\n'
                    info_text += ''.join(f'{key}: {info[key]}\n' for key in info)
                    info_text += '\nFiles:\n'
                    info_text += 'META/info.json\n'
                    if image:
                        info_text += 'META/image.png\n'
                    if len(wads) > 0:
                        info_text += ''.join(f'{wad_name}\n' for wad_name in wads)
                    info_text += '\n\n'
                    tk_widgets.VH.scanned_fantomes.append(fantome_path)
                except Exception as e:
                    info_text += '\n'+str(e) + '\n\n'
            tk_widgets.VH.info_text.configure(state=tk.NORMAL)
            tk_widgets.VH.info_text.delete('1.0', tk.END)
            tk_widgets.VH.info_text.insert(tk.END, info_text)
            tk_widgets.VH.info_text.configure(state=tk.DISABLED)
        else:
            tk_widgets.VH.info_text.configure(state=tk.NORMAL)
            tk_widgets.VH.info_text.delete('1.0', tk.END)
            tk_widgets.VH.info_text.configure(state=tk.DISABLED)
        tk_widgets.VH.input_entry.delete(0, tk.END)
        tk_widgets.VH.input_entry.insert(tk.END, dir_path)
    # create browse folder button
    tk_widgets.VH.browsefolder_button = ctk.CTkButton(
        tk_widgets.VH.input_frame,
        text='Browse Folder of FANTOMEs/ZIPs',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=browsefolder_cmd,
        font=le_font
    )
    tk_widgets.VH.browsefolder_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # create info text
    tk_widgets.VH.info_text = ctk.CTkTextbox(
        tk_widgets.VH.page_frame,
        state=tk.DISABLED,
        wrap=tk.NONE,
        font=le_font,
    )
    tk_widgets.VH.info_text.configure(state=tk.NORMAL)
    tk_widgets.VH.info_text.insert(tk.END, 'Starting from patch 14.4, rito decided to use en_us for all clients/regions.\nSo this tool is not needed anymore except for updating old mods before 14.4.')
    tk_widgets.VH.info_text.configure(state=tk.DISABLED)
    tk_widgets.VH.info_text.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create action frame
    tk_widgets.VH.action_frame = ctk.CTkFrame(
        tk_widgets.VH.page_frame, fg_color=TRANSPARENT)
    tk_widgets.VH.action_frame.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.VH.action_frame.rowconfigure(0, weight=1)
    tk_widgets.VH.action_frame.columnconfigure(0, weight=1)
    tk_widgets.VH.action_frame.columnconfigure(1, weight=1)
    tk_widgets.VH.action_frame.columnconfigure(2, weight=699)
    tk_widgets.VH.action_frame.columnconfigure(3, weight=1)

    # create target options
    tk_widgets.VH.target_option = ctk.CTkOptionMenu(
        tk_widgets.VH.action_frame,
        values=vo_helper.LANGS,
        font=le_font
    )
    tk_widgets.VH.target_option.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def target_cmd():
        if not check_thread_safe(tk_widgets.VH.making_thread):
            LOG(
                'vo_helper: Failed: Remake Fantomes: A thread is already running, wait for it to finished.')
            return
        
        def make_thrd():
            for fantome_path in tk_widgets.VH.scanned_fantomes:
                fantome_name = os.path.basename(fantome_path)
                output_dir_path = fantome_path.replace('.fantome', '') + " VO HELPER"
                os.makedirs(output_dir_path, exist_ok=True)
                LOG(f'vo_helper: Running: Remake FANTOME {fantome_path}')
                info, image, wads = vo_helper.read_fantome(fantome_path)
                vo_helper.make_fantome(
                    fantome_name, output_dir_path, info, image, wads, [tk_widgets.VH.target_option.get()])

        tk_widgets.VH.making_thread = Thread(target=make_thrd, daemon=True)
        tk_widgets.VH.making_thread.start()

    # create target button
    tk_widgets.VH.target_button = ctk.CTkButton(
        tk_widgets.VH.action_frame,
        text='Remake For Selected Lang',
        image=EmojiImage.create('🦎'),
        command=target_cmd,
        font=le_font
    )
    tk_widgets.VH.target_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def make_cmd():
        if not check_thread_safe(tk_widgets.VH.making_thread):
            LOG(
                'vo_helper: Failed: Remake Fantomes: A thread is already running, wait for it to finished.')
            return
        
        def make_thrd():
            for fantome_path in tk_widgets.VH.scanned_fantomes:
                fantome_name = os.path.basename(fantome_path)
                output_dir_path = fantome_path.replace('.fantome', '') + " VO HELPER"
                os.makedirs(output_dir_path, exist_ok=True)
                LOG(f'vo_helper: Running: Remake FANTOME {fantome_path}')
                info, image, wads = vo_helper.read_fantome(fantome_path)
                vo_helper.make_fantome(
                    fantome_name, output_dir_path, info, image, wads, vo_helper.LANGS)

        tk_widgets.VH.making_thread = Thread(target=make_thrd, daemon=True)
        tk_widgets.VH.making_thread.start()

    # create make all button
    tk_widgets.VH.make_button = ctk.CTkButton(
        tk_widgets.VH.action_frame,
        text='Remake For All Langs',
        image=EmojiImage.create('🦖'),
        command=make_cmd,
        font=le_font
    )
    tk_widgets.VH.make_button.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)


def create_NS_page():
    # create page frame
    tk_widgets.NS.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.NS.page_frame.columnconfigure(0, weight=1)
    tk_widgets.NS.page_frame.rowconfigure(0, weight=1)

    # create tab view
    tk_widgets.NS.tabview = ctk.CTkTabview(
        tk_widgets.NS.page_frame
    )
    tk_widgets.NS.tabview.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    # create tab1 frame
    tk_widgets.NS.tab1 = tk_widgets.NS.tabview.add('No skin full')
    tk_widgets.NS.tab1.columnconfigure(0, weight=1)
    tk_widgets.NS.tab1.rowconfigure(0, weight=1)
    tk_widgets.NS.tab1_frame = ctk.CTkFrame(
        tk_widgets.NS.tab1,
        fg_color=TRANSPARENT,
    )
    tk_widgets.NS.tab1_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.NS.tab1_frame.columnconfigure(0, weight=1)
    tk_widgets.NS.tab1_frame.rowconfigure(0, weight=1)
    tk_widgets.NS.tab1_frame.rowconfigure(1, weight=1)
    tk_widgets.NS.tab1_frame.rowconfigure(2, weight=699)

    # init stuffs
    tk_widgets.NS.working_thread = None
    # create input frame
    tk_widgets.NS.input_frame = ctk.CTkFrame(
        tk_widgets.NS.tab1_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.NS.input_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.NS.input_frame.columnconfigure(0, weight=9)
    tk_widgets.NS.input_frame.columnconfigure(1, weight=1)
    # create champions folder entry
    tk_widgets.NS.cfolder_entry = ctk.CTkEntry(
        tk_widgets.NS.input_frame,
        font=le_font
    )
    tk_widgets.NS.cfolder_entry.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    cfolder = setting.get('game_folder', '')
    if cfolder != '':
        tk_widgets.NS.cfolder_entry.insert(
            tk.END, cfolder + '/DATA/FINAL/Champions')

    def browse_cmd():
        skl_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select Folder: League of Legends/Game/DATA/FINAL/Champions',
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.NS.cfolder_entry.delete(0, tk.END)
        tk_widgets.NS.cfolder_entry.insert(tk.END, skl_path)
    # create browse button
    tk_widgets.NS.browse_button = ctk.CTkButton(
        tk_widgets.NS.input_frame,
        text='Browse Champions folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=browse_cmd,
        font=le_font
    )
    tk_widgets.NS.browse_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create action frame
    tk_widgets.NS.action_frame = ctk.CTkFrame(
        tk_widgets.NS.tab1_frame, fg_color=TRANSPARENT)
    tk_widgets.NS.action_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.NS.action_frame.columnconfigure(0, weight=1)
    tk_widgets.NS.action_frame.columnconfigure(1, weight=699)
    tk_widgets.NS.action_frame.columnconfigure(2, weight=1)

    def save_skips_cmd():
        no_skin.set_skips(
            tk_widgets.NS.skips_textbox.get('1.0', tk.END))
        no_skin.save_skips()
        LOG('no_skin: Done: Save SKIPS.json')
    # create save SKIPS button
    tk_widgets.NS.save_skips_button = ctk.CTkButton(
        tk_widgets.NS.action_frame,
        text='Save SKIPS',
        image=EmojiImage.create('💾'),
        command=save_skips_cmd,
        font=le_font
    )
    tk_widgets.NS.save_skips_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def start_cmd():
        if check_thread_safe(tk_widgets.NS.working_thread):
            dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Output Folder',
                initialdir=setting.get('default_folder', None)
            )
            if dir_path != '':
                def working_thrd():
                    Log.tk_cooldown = 5000
                    no_skin.parse(tk_widgets.NS.cfolder_entry.get(), dir_path)
                    Log.tk_cooldown = 0
                    LOG(f'no_skin: Done: Created {dir_path}')
                tk_widgets.NS.working_thread = Thread(
                    target=working_thrd,
                    daemon=True
                )
                tk_widgets.NS.working_thread.start()
        else:
            LOG(
                'no_skin: Failed: A thread is already running, wait for it to finished.')
    # create start button
    tk_widgets.NS.start_button = ctk.CTkButton(
        tk_widgets.NS.action_frame,
        text='Start',
        image=EmojiImage.create('🐧'),
        command=start_cmd,
        font=le_font
    )
    tk_widgets.NS.start_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # create skips textbox
    tk_widgets.NS.skips_textbox = ctk.CTkTextbox(
        tk_widgets.NS.tab1_frame,
        wrap=tk.NONE,
        font=le_font
    )

    def tab_pressed():
        tk_widgets.NS.skips_textbox.insert('insert', ' '*4)
        return 'break'
    tk_widgets.NS.skips_textbox.bind(
        '<Tab>', lambda e: tab_pressed())
    tk_widgets.NS.skips_textbox.insert(tk.END, no_skin.get_skips())
    tk_widgets.NS.skips_textbox.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)


    # create tab2 frame
    tk_widgets.NS.tab2 = tk_widgets.NS.tabview.add('No skin lite')
    tk_widgets.NS.tab2.columnconfigure(0, weight=1)
    tk_widgets.NS.tab2.rowconfigure(0, weight=1)
    tk_widgets.NS.tab2_frame = ctk.CTkFrame(
        tk_widgets.NS.tab2,
        fg_color=TRANSPARENT,
    )
    tk_widgets.NS.tab2_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.NS.tab2_frame.columnconfigure(0, weight=699)
    tk_widgets.NS.tab2_frame.columnconfigure(1, weight=1)
    tk_widgets.NS.tab2_frame.rowconfigure(0, weight=1)
    tk_widgets.NS.tab2_frame.rowconfigure(1, weight=699)
    tk_widgets.NS.tab2_frame.rowconfigure(2, weight=1)

    # create skin0 label
    tk_widgets.NS.skin0_label = ctk.CTkLabel(
        tk_widgets.NS.tab2_frame,
        justify=tk.LEFT,
        anchor=tk.W,
        text='',
        font=le_font
    )
    tk_widgets.NS.skin0_label.grid(
        row=0, column=0, padx=10, pady=5, sticky=tk.NSEW)
    
    def skin0_cmd():
        bin_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select your Animation BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.NS.skin0_label.configure(text=bin_path)
    # create skin0 button
    tk_widgets.NS.skin0_button = ctk.CTkButton(
        tk_widgets.NS.tab2_frame,
        text='Select Skin0 BIN',
        image=EmojiImage.create('📝'),
        command=skin0_cmd,
        font=le_font
    )
    tk_widgets.NS.skin0_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    
    # create otherskins text
    tk_widgets.NS.otherskins_text = ctk.CTkTextbox(
        tk_widgets.NS.tab2_frame,
        state=tk.DISABLED,
        wrap=tk.WORD,
        fg_color=TRANSPARENT,
        font=le_font
    )
    tk_widgets.NS.otherskins_text.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    def otherskins_cmd():
        bin_paths = tkfd.askopenfilenames(
            parent=tk_widgets.main_tk,
            title='Select your Animation BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.NS.otherskins_text.configure(state=tk.NORMAL)
        tk_widgets.NS.otherskins_text.delete('1.0', tk.END)
        tk_widgets.NS.otherskins_text.insert('1.0', '\n'.join(bin_paths))
        tk_widgets.NS.otherskins_text.configure(state=tk.DISABLED)
    # create otherskins button
    tk_widgets.NS.otherskins_button = ctk.CTkButton(
        tk_widgets.NS.tab2_frame,
        text='Select Other Skin BINs',
        image=EmojiImage.create('📝'),
        command=otherskins_cmd,
        font=le_font
    )
    tk_widgets.NS.otherskins_button.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.N+tk.EW)
    
    def do_cmd():
        if check_thread_safe(tk_widgets.NS.working_thread):
            def working_thrd():
                try:
                    no_skin.mini_no_skin(
                        skin0_file=tk_widgets.NS.skin0_label.cget('text'), 
                        otherskins_files=tk_widgets.NS.otherskins_text.get('1.0', 'end-1c').split('\n')
                    )
                except Exception as e:
                    LOG(str(e))
            tk_widgets.NS.working_thread = Thread(
                target=working_thrd,
                daemon=True
            )
            tk_widgets.NS.working_thread.start()
        else:
            LOG(
                'no_skin: Failed: A thread is already running, wait for it to finished.')
    # create do button
    tk_widgets.NS.do_button = ctk.CTkButton(
        tk_widgets.NS.tab2_frame,
        text='DEW IT',
        image=EmojiImage.create('🦭'),
        command=do_cmd,
        font=le_font
    )
    tk_widgets.NS.do_button.grid(
        row=2, column=1, padx=5, pady=5, sticky=tk.NSEW)
    

def create_UVEE_page():
    # create page frame
    tk_widgets.UVEE.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.UVEE.page_frame.columnconfigure(0, weight=1)
    tk_widgets.UVEE.page_frame.rowconfigure(0, weight=1)
    tk_widgets.UVEE.page_frame.rowconfigure(1, weight=699)
    # handle drop in UVEE
    def page_drop_cmd(event):
        paths = dnd_return_handle(event.data)
        fgs = []
        for path in paths:
            path = path.replace('\\', '/')
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.skn') or file.endswith('.sco') or file.endswith('.scb'): 
                            fgs.append(read_file(os.path.join(root, file).replace('\\', '/')))
            else:
                if path.endswith('.skn') or path.endswith('.sco') or path.endswith('.scb'):
                    fgs.append(read_file(path))
        for fg in fgs:
            fg()
    tk_widgets.UVEE.page_frame.drop_target_register(tkdnd.DND_FILES)
    tk_widgets.UVEE.page_frame.dnd_bind('<<Drop>>', page_drop_cmd)
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
            return lambda: None
        # id of this file
        file_frame_id = len(tk_widgets.UVEE.loaded_files)
        # create file frame
        file_frame = ctk.CTkFrame(
            tk_widgets.UVEE.view_frame
        )
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
            width=30,
            text='',
            image=EmojiImage.create('🔽'),
            fg_color=TRANSPARENT,
            command=lambda: view_cmd(file_frame_id)
        )
        view_button.grid(row=0, column=0, padx=2,
                         pady=2, sticky=tk.W)
        # create file label
        file_label = ctk.CTkLabel(
            head_frame,
            text=file_path,
            anchor=tk.W,
            justify=tk.LEFT,
            font=le_font
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
            width=30,
            text='',
            image=EmojiImage.create('❌'),
            fg_color=TRANSPARENT,
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
                fg_color='black',
                font=le_font
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
        return lambda id=file_frame_id: file_frame.grid(row=id, column=0, padx=2, pady=5, sticky=tk.NSEW)

    def fileread_cmd():
        file_paths = tkfd.askopenfilenames(
            parent=tk_widgets.main_tk,
            title='Select SKN/SCO/SCB File To Extract',
            filetypes=(
                ('SKN/SCO/SCB files',
                    (
                        '*.skn',
                        '*.sco',
                        '*.scb',
                    )
                 ),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        if len(file_paths) > 0:
            fgs = []
            for file_path in file_paths:
                fgs.append(read_file(file_path))
            for fg in fgs:
                fg()
    # create file read button
    tk_widgets.UVEE.fileread_button = ctk.CTkButton(
        tk_widgets.UVEE.input_frame,
        text='Extract UVs From Files',
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=fileread_cmd,
        font=le_font
    )
    tk_widgets.UVEE.fileread_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def folderread_cmd():
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select Folder To Extract',
            initialdir=setting.get('default_folder', None)
        )
        if dir_path != '':
            fgs = []
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('.skn') or file.endswith('.sco') or file.endswith('.scb'):
                        fgs.append(read_file(os.path.join(root, file).replace('\\', '/')))
            for fg in fgs:
                fg()
                
    # create folder read button
    tk_widgets.UVEE.folderread_button = ctk.CTkButton(
        tk_widgets.UVEE.input_frame,
        text='Extract UVs From Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=folderread_cmd,
        font=le_font
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
        LOG(f'yvee: Done: Cleared all loaded images.')
    # create clear button
    tk_widgets.UVEE.clear_button = ctk.CTkButton(
        tk_widgets.UVEE.input_frame,
        text='Clear Loaded Images',
        image=EmojiImage.create('❌'),
        anchor=tk.CENTER,
        command=clear_cmd,
        font=le_font
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
        command=lef_cmd,
        font=le_font
    )
    tk_widgets.UVEE.load_extracted_files = setting.get(
        'Uvee.load_extracted_files', False)
    if tk_widgets.UVEE.load_extracted_files:
        tk_widgets.UVEE.lef_switch.select()
    else:
        tk_widgets.UVEE.lef_switch.deselect()
    tk_widgets.UVEE.lef_switch.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)


def create_SHR_page():
    # create page frame
    tk_widgets.SHR.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.SHR.page_frame.columnconfigure(0, weight=1)
    tk_widgets.SHR.page_frame.rowconfigure(0, weight=1)
    tk_widgets.SHR.page_frame.rowconfigure(1, weight=699)
    tk_widgets.SHR.page_frame.rowconfigure(2, weight=1)
    # init stuffs
    tk_widgets.SHR.working_thread = None
    # create input frame
    tk_widgets.SHR.input_frame = ctk.CTkFrame(
        tk_widgets.SHR.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.SHR.input_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SHR.input_frame.rowconfigure(0, weight=1)
    tk_widgets.SHR.input_frame.columnconfigure(0, weight=12)
    tk_widgets.SHR.input_frame.columnconfigure(1, weight=1)
    tk_widgets.SHR.input_frame.columnconfigure(2, weight=1)
    # create input entry
    tk_widgets.SHR.input_entry = ctk.CTkEntry(
        tk_widgets.SHR.input_frame,
        font=le_font
    )
    tk_widgets.SHR.input_entry.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def browsefile_cmd():
        anm_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select ANM file',
            filetypes=(
                ('ANM files', '*.anm'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.SHR.input_entry.delete(0, tk.END)
        tk_widgets.SHR.input_entry.insert(tk.END, anm_path)
    # create browse file button
    tk_widgets.SHR.browsefile_button = ctk.CTkButton(
        tk_widgets.SHR.input_frame,
        text='Browse ANM',
        image=EmojiImage.create('🦿'),
        anchor=tk.CENTER,
        command=browsefile_cmd,
        font=le_font
    )
    tk_widgets.SHR.browsefile_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def browsefolder_cmd():
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select Folder of ANMs',
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.SHR.input_entry.delete(0, tk.END)
        tk_widgets.SHR.input_entry.insert(tk.END, dir_path)
    # create browse folder button
    tk_widgets.SHR.browsefolder_button = ctk.CTkButton(
        tk_widgets.SHR.input_frame,
        text='Browse Folder of ANMs',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=browsefolder_cmd,
        font=le_font
    )
    tk_widgets.SHR.browsefolder_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # create mid frame
    tk_widgets.SHR.mid_frame = ctk.CTkFrame(
        tk_widgets.SHR.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.SHR.mid_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SHR.mid_frame.rowconfigure(0, weight=699)
    tk_widgets.SHR.mid_frame.rowconfigure(1, weight=1)
    tk_widgets.SHR.mid_frame.rowconfigure(2, weight=1)
    tk_widgets.SHR.mid_frame.columnconfigure(0, weight=1)
    tk_widgets.SHR.mid_frame.columnconfigure(1, weight=1)
    # create old textbox
    tk_widgets.SHR.old_text = ctk.CTkTextbox(
        tk_widgets.SHR.mid_frame,
        wrap=tk.NONE,
        font=le_font
    )
    tk_widgets.SHR.old_text.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def old_skl_cmd():
        skl_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select SKL file',
            filetypes=(
                ('SKL files', '*.skl'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        if skl_path != '':
            skl = pyRitoFile.read_skl(skl_path)
            tk_widgets.SHR.old_text.insert(tk.END,
                                           '\n'.join(joint.name for joint in skl.joints))
    # create old skl button
    tk_widgets.SHR.old_skl_button = ctk.CTkButton(
        tk_widgets.SHR.mid_frame,
        text='Load old SKL joints',
        image=EmojiImage.create('🦴'),
        command=old_skl_cmd,
        font=le_font
    )
    tk_widgets.SHR.old_skl_button.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create new textbox
    tk_widgets.SHR.new_text = ctk.CTkTextbox(
        tk_widgets.SHR.mid_frame,
        wrap=tk.NONE,
        font=le_font
    )
    tk_widgets.SHR.new_text.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def new_skl_cmd():
        skl_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select SKL file',
            filetypes=(
                ('SKL files', '*.skl'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        if skl_path != '':
            skl = pyRitoFile.read_skl(skl_path)
            tk_widgets.SHR.new_text.insert(tk.END,
                                           '\n'.join(joint.name for joint in skl.joints))
    # create new skl button
    tk_widgets.SHR.new_skl_button = ctk.CTkButton(
        tk_widgets.SHR.mid_frame,
        text='Load new SKL joints',
        image=EmojiImage.create('🦴'),
        command=new_skl_cmd,
        font=le_font
    )
    tk_widgets.SHR.new_skl_button.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create action frame
    tk_widgets.SHR.action_frame = ctk.CTkFrame(
        tk_widgets.SHR.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.SHR.action_frame.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SHR.action_frame.rowconfigure(0, weight=1)
    tk_widgets.SHR.action_frame.columnconfigure(0, weight=1)
    tk_widgets.SHR.action_frame.columnconfigure(1, weight=699)
    tk_widgets.SHR.action_frame.columnconfigure(2, weight=1)

    def rename_cmd():
        if check_thread_safe(tk_widgets.SHR.working_thread):
            def rename_thrd():
                olds = tk_widgets.SHR.old_text.get('1.0', 'end-1c').split('\n')
                news = tk_widgets.SHR.new_text.get('1.0', 'end-1c').split('\n')
                length = min(len(olds), len(news))
                path = tk_widgets.SHR.input_entry.get()
                if length > 0 and path != '':
                    shrum.rename(path,
                                 olds[:length], news[:length], setting.get('Shrum.backup', 1))
            tk_widgets.SHR.working_thread = Thread(
                target=rename_thrd, daemon=True)
            tk_widgets.SHR.working_thread.start()
        else:
            LOG(
                'shrum: Failed: Rename: A thread is already running, wait for it to finished.')

    # create rename button
    tk_widgets.SHR.rename_button = ctk.CTkButton(
        tk_widgets.SHR.action_frame,
        text='Rename Joints in ANMS',
        image=EmojiImage.create('🍄'),
        command=rename_cmd,
        font=le_font
    )
    tk_widgets.SHR.rename_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

    def backup_cmd():
        setting.set('Shrum.backup', tk_widgets.SHR.backup_switch.get())
        setting.save()
    # create backup switch
    tk_widgets.SHR.backup_switch = ctk.CTkSwitch(
        tk_widgets.SHR.action_frame,
        text='Create backup before rename (safe)',
        command=backup_cmd,
        font=le_font
    )
    if setting.get('Shrum.backup', 1) == 1:
        tk_widgets.SHR.backup_switch.select()
    else:
        tk_widgets.SHR.backup_switch.deselect()
    tk_widgets.SHR.backup_switch.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)


def create_HP_page():
    tk_widgets.HP.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.HP.page_frame.columnconfigure(0, weight=1)
    tk_widgets.HP.page_frame.rowconfigure(0, weight=1)
    tk_widgets.HP.page_frame.rowconfigure(1, weight=1)
    tk_widgets.HP.page_frame.rowconfigure(2, weight=1)
    tk_widgets.HP.page_frame.rowconfigure(3, weight=699)
    # init stuffs
    tk_widgets.HP.working_thread = None

    # create action frame
    tk_widgets.HP.action_frame = ctk.CTkFrame(
        tk_widgets.HP.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.HP.action_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HP.action_frame.columnconfigure(0, weight=999)
    tk_widgets.HP.action_frame.columnconfigure(1, weight=1)
    tk_widgets.HP.action_frame.rowconfigure(0, weight=1)
    # create backup switch
    def backup_cmd():
        setting.set('hapiBin.backup', tk_widgets.HP.backup_switch.get())
        setting.save()
    tk_widgets.HP.backup_switch = ctk.CTkSwitch(
        tk_widgets.HP.action_frame,
        text='Do the backup thing',
        command=backup_cmd,
        font=le_font
    )
    if setting.get('hapiBin.backup', 1) == 1:
        tk_widgets.HP.backup_switch.select()
    else:
        tk_widgets.HP.backup_switch.deselect()
    tk_widgets.HP.backup_switch.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    
    # create input description label 
    tk_widgets.HP.input_description_label = ctk.CTkLabel(
        tk_widgets.HP.page_frame,
        text='Selected source type must match target type.\n    BIN: run functions directly on selected BIN.\n    WAD/FOLDER: run functions on all bins inside selected WAD/FOLDER.',
        anchor=tk.NW,
        justify=tk.LEFT,
        font=le_font
    )
    tk_widgets.HP.input_description_label.grid(
        row=1, column=0, padx=20, pady=0, sticky=tk.NSEW)

    # create input frame
    tk_widgets.HP.input_frame = ctk.CTkFrame(
        tk_widgets.HP.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.HP.input_frame.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HP.input_frame.columnconfigure(0, weight=1)
    tk_widgets.HP.input_frame.rowconfigure(0, weight=1)
    tk_widgets.HP.input_frame.rowconfigure(1, weight=1)
    tk_widgets.HP.input_frame.rowconfigure(2, weight=1)
    tk_widgets.HP.input_frame.rowconfigure(3, weight=1)

    # create source entry
    tk_widgets.HP.source_entry = ctk.CTkEntry(
        tk_widgets.HP.input_frame,
        font=le_font
    )
    tk_widgets.HP.source_entry.grid( 
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create source frame
    tk_widgets.HP.source_frame = ctk.CTkFrame(
        tk_widgets.HP.input_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.HP.source_frame.grid(
        row=1, column=0, padx=0, pady=0, sticky=tk.NSEW)
    tk_widgets.HP.source_frame.columnconfigure(0, weight=999)
    tk_widgets.HP.source_frame.columnconfigure(1, weight=1)
    tk_widgets.HP.source_frame.columnconfigure(2, weight=1)
    tk_widgets.HP.source_frame.columnconfigure(3, weight=1)
    tk_widgets.HP.source_frame.rowconfigure(0, weight=1)
    # create source bin button
    def source_bin_cmd():
        bin_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select source BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.HP.source_entry.delete(0, tk.END)
        tk_widgets.HP.source_entry.insert(tk.END, bin_path)
    tk_widgets.HP.source_bin_button = ctk.CTkButton(
        tk_widgets.HP.source_frame,
        text='Browse Source BIN',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=source_bin_cmd,
        font=le_font
    )
    tk_widgets.HP.source_bin_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create source wad button
    def source_wad_cmd():
        wad_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select source WAD file',
            filetypes=(
                ('WAD files', '*.wad.client'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.HP.source_entry.delete(0, tk.END)
        tk_widgets.HP.source_entry.insert(tk.END, wad_path)
    tk_widgets.HP.source_wad_button = ctk.CTkButton(
        tk_widgets.HP.source_frame,
        text='Browse Source WAD',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=source_wad_cmd,
        font=le_font
    )
    tk_widgets.HP.source_wad_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # create source dir button
    def source_dir_cmd():
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select source Folder',
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.HP.source_entry.delete(0, tk.END)
        tk_widgets.HP.source_entry.insert(tk.END, dir_path)
    tk_widgets.HP.source_dir_button = ctk.CTkButton(
        tk_widgets.HP.source_frame,
        text='Browse Source FOLDER',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=source_dir_cmd,
        font=le_font
    )
    tk_widgets.HP.source_dir_button.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)


    # create target entry
    tk_widgets.HP.target_entry = ctk.CTkEntry(
        tk_widgets.HP.input_frame,
        font=le_font
    )
    tk_widgets.HP.target_entry.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create target frame
    tk_widgets.HP.target_frame = ctk.CTkFrame(
        tk_widgets.HP.input_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.HP.target_frame.grid(
        row=3, column=0, padx=0, pady=0, sticky=tk.NSEW)
    tk_widgets.HP.target_frame.columnconfigure(0, weight=999)
    tk_widgets.HP.target_frame.columnconfigure(1, weight=1)
    tk_widgets.HP.target_frame.columnconfigure(2, weight=1)
    tk_widgets.HP.target_frame.columnconfigure(3, weight=1)
    tk_widgets.HP.target_frame.rowconfigure(0, weight=1)
    # create target bin button
    def target_bin_cmd():
        bin_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select target BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.HP.target_entry.delete(0, tk.END)
        tk_widgets.HP.target_entry.insert(tk.END, bin_path)
    tk_widgets.HP.target_bin_button = ctk.CTkButton(
        tk_widgets.HP.target_frame,
        text='Browse Target BIN',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=target_bin_cmd,
        font=le_font
    )
    tk_widgets.HP.target_bin_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create target wad button
    def target_wad_cmd():
        wad_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select target WAD file',
            filetypes=(
                ('WAD files', '*.wad.client'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.HP.target_entry.delete(0, tk.END)
        tk_widgets.HP.target_entry.insert(tk.END, wad_path)
    tk_widgets.HP.target_wad_button = ctk.CTkButton(
        tk_widgets.HP.target_frame,
        text='Browse Target WAD',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=target_wad_cmd,
        font=le_font
    )
    tk_widgets.HP.target_wad_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # create target dir button
    def target_dir_cmd():
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select target Folder',
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.HP.target_entry.delete(0, tk.END)
        tk_widgets.HP.target_entry.insert(tk.END, dir_path)
    tk_widgets.HP.target_dir_button = ctk.CTkButton(
        tk_widgets.HP.target_frame,
        text='Browse Target FOLDER',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=target_dir_cmd,
        font=le_font
    )
    tk_widgets.HP.target_dir_button.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)
    
    # create func frame 
    tk_widgets.HP.func_frame = ctk.CTkScrollableFrame(
        tk_widgets.HP.page_frame, fg_color=TRANSPARENT)
    tk_widgets.HP.func_frame.grid(
        row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HP.func_frame.columnconfigure(0, weight=1)

    def run_hp_command(hp_command, require_dst):
        if check_thread_safe(tk_widgets.HP.working_thread):
            def working_thrd():
                hapiBin.HPHelper.main(
                    src=tk_widgets.HP.source_entry.get(), 
                    dst=tk_widgets.HP.target_entry.get(),
                    hp_command=hp_command, 
                    require_dst=require_dst, 
                    backup=setting.get('hapiBin.backup', 1)
                )
            tk_widgets.HP.working_thread = Thread(
                target=working_thrd, daemon=True
            )
            tk_widgets.HP.working_thread.start()
        else:
            LOG(
                'hapiBin: Failed: A thread is already running, wait for it to finished.')

    # create hp funcs
    for func_id, (label, descritpion, icon, hp_command, require_dst) in enumerate(hapiBin.tk_widgets_data):
        func_frame = ctk.CTkFrame(
            tk_widgets.HP.func_frame
        )
        func_frame.grid(row=func_id, column=0, padx=5, pady=5, sticky=tk.NSEW)
        tk_widgets.HP.func_frame.rowconfigure(func_id, weight=1)
        func_frame.rowconfigure(0, weight=1)
        func_frame.rowconfigure(1, weight=1)
        func_frame.columnconfigure(0, weight=1)
        func_button = ctk.CTkButton(
            func_frame,
            text=label,
            command=lambda hp_command=hp_command, require_dst=require_dst: run_hp_command(hp_command, require_dst),
            image=EmojiImage.create(icon),
            font=le_font
        )
        func_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NS+tk.W)
        func_label = ctk.CTkLabel(
            func_frame,
            text=descritpion,
            anchor=tk.NW,
            justify=tk.LEFT,
            font=le_font
        )
        func_label.grid(row=1, column=0, padx=10, pady=0, sticky=tk.NS+tk.W)
    tk_widgets.HP.func_frame.rowconfigure(len(hapiBin.tk_widgets_data), weight=699)

    # handle drop in HP
    def entry_drop_cmd(event, entry):
        entry_path = dnd_return_handle(event.data)[0]
        if entry_path.endswith('.bin') or entry_path.endswith('.wad.client') or os.path.isdir(entry_path):
            entry.delete(0, tk.END)
            entry.insert(tk.END, entry_path)
    tk_widgets.HP.source_entry.drop_target_register(tkdnd.DND_FILES)
    tk_widgets.HP.source_entry.dnd_bind('<<Drop>>', lambda event: entry_drop_cmd(event, tk_widgets.HP.source_entry))
    tk_widgets.HP.target_entry.drop_target_register(tkdnd.DND_FILES)
    tk_widgets.HP.target_entry.dnd_bind('<<Drop>>', lambda event: entry_drop_cmd(event, tk_widgets.HP.target_entry))


def create_WT_page():
    # create page frame
    tk_widgets.WT.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.WT.page_frame.columnconfigure(0, weight=1)
    tk_widgets.WT.page_frame.rowconfigure(0, weight=1)
    tk_widgets.WT.page_frame.rowconfigure(1, weight=699)
    # handle drop in WT
    def page_drop_cmd(event):
        def page_drop_thrd():
            hash_manager.read_wad_hashes()
            paths = dnd_return_handle(event.data)
            for path in paths:
                path = path.replace('\\', '/')
                if os.path.isdir(path):
                    src = path
                    dst = src
                    if dst.endswith('.wad'):
                        dst += '.client'
                    else:
                        if not dst.endswith('.wad.client'):
                            dst += '.wad.client'
                    Log.tk_cooldown = 5000
                    wad_tool.pack(src, dst)
                    Log.tk_cooldown = 0
                    LOG(
                        f'wad_tool: Done: Pack {src}')
                elif os.path.isfile(path) and path.endswith('.wad.client'):
                    Log.tk_cooldown = 5000
                    src = path
                    dst = src.replace('.wad.client', '.wad')
                    wad_tool.unpack(src, dst, hash_manager.HASHTABLES)
                    Log.tk_cooldown = 0
                    LOG(
                        f'wad_tool: Done: Unpack {src}')
            hash_manager.free_wad_hashes()   

        if check_thread_safe(tk_widgets.WT.working_thread):
            tk_widgets.WT.working_thread = Thread(
                target=page_drop_thrd,
                daemon=True
            )
            tk_widgets.WT.working_thread.start()
        else:
            LOG('wad_tool: Failed: A thread is already running, wait for it to finished.')
    tk_widgets.WT.page_frame.drop_target_register(tkdnd.DND_FILES)
    tk_widgets.WT.page_frame.dnd_bind('<<Drop>>', page_drop_cmd)
    # init stuffs
    tk_widgets.WT.working_thread = None
    tk_widgets.WT.loaded_wads = []
    tk_widgets.WT.loaded_wad_paths = []
    tk_widgets.WT.loaded_chunk_hashes = []
    # create action frame
    tk_widgets.WT.action_frame = ctk.CTkFrame(
        tk_widgets.WT.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.WT.action_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.WT.action_frame.rowconfigure(0, weight=1)
    tk_widgets.WT.action_frame.columnconfigure(0, weight=1)
    tk_widgets.WT.action_frame.columnconfigure(1, weight=1)
    tk_widgets.WT.action_frame.columnconfigure(2, weight=699)

    def wad2dir_cmd():
        if check_thread_safe(tk_widgets.WT.working_thread):
            file_paths = tkfd.askopenfilenames(
                parent=tk_widgets.main_tk,
                title='Select WADs To Unpack',
                filetypes=(
                    ('WAD files', '*.wad.client'),
                    ('All files', '*.*'),
                ),
                initialdir=setting.get('default_folder', None)
            )
            if len(file_paths) > 0:
                def working_thrd():
                    hash_manager.read_wad_hashes()
                    Log.tk_cooldown = 5000
                    for file_path in file_paths:
                        src = file_path
                        dst = src.replace('.wad.client', '.wad')
                        wad_tool.unpack(src, dst, hash_manager.HASHTABLES)
                        LOG(
                            f'wad_tool: Done: Unpack {src}')
                    Log.tk_cooldown = 0
                    hash_manager.free_wad_hashes()
                tk_widgets.WT.working_thread = Thread(
                    target=working_thrd,
                    daemon=True
                )
                tk_widgets.WT.working_thread.start()
        else:
            LOG(
                'wad_tool: Failed: A thread is already running, wait for it to finished.')
    # create wad to folder button
    tk_widgets.WT.wad2dir_button = ctk.CTkButton(
        tk_widgets.WT.action_frame,
        text='WAD to Folder',
        image=EmojiImage.create('📦'),
        anchor=tk.CENTER,
        command=wad2dir_cmd,
        font=le_font
    )
    tk_widgets.WT.wad2dir_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def dir2wad_cmd():
        if check_thread_safe(tk_widgets.WT.working_thread):
            dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Folder To Pack',
                initialdir=setting.get('default_folder', None)
            )
            if dir_path != '':
                def working_thrd():
                    src = dir_path
                    dst = src
                    if dst.endswith('.wad'):
                        dst += '.client'
                    else:
                        if not dst.endswith('.wad.client'):
                            dst += '.wad.client'
                    Log.tk_cooldown = 5000
                    wad_tool.pack(src, dst)
                    Log.tk_cooldown = 0
                    LOG(
                        f'wad_tool: Done: Pack {src}')
                tk_widgets.WT.working_thread = Thread(
                    target=working_thrd,
                    daemon=True
                )
                tk_widgets.WT.working_thread.start()
        else:
            LOG(
                'wad_tool: Failed: A thread is already running, wait for it to finished.')
    # create folder to wad button
    tk_widgets.WT.dir2wad_button = ctk.CTkButton(
        tk_widgets.WT.action_frame,
        text='Folder to WAD',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=dir2wad_cmd,
        font=le_font
    )
    tk_widgets.WT.dir2wad_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create action2 frame
    tk_widgets.WT.action2_frame = ctk.CTkFrame(
        tk_widgets.WT.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.WT.action2_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.WT.action2_frame.rowconfigure(0, weight=1)
    tk_widgets.WT.action2_frame.rowconfigure(1, weight=1)
    tk_widgets.WT.action2_frame.rowconfigure(2, weight=699)
    tk_widgets.WT.action2_frame.rowconfigure(3, weight=1)
    tk_widgets.WT.action2_frame.columnconfigure(0, weight=1)
    # create bulk label
    tk_widgets.WT.bulk_label = ctk.CTkLabel(
        tk_widgets.WT.action2_frame,
        text='Bulk unpack WADs to same Folder',
        font=le_font
    )
    tk_widgets.WT.bulk_label.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create action3 frame
    tk_widgets.WT.action3_frame = ctk.CTkFrame(
        tk_widgets.WT.action2_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.WT.action3_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.WT.action3_frame.rowconfigure(0, weight=1)
    tk_widgets.WT.action3_frame.columnconfigure(0, weight=1)
    tk_widgets.WT.action3_frame.columnconfigure(1, weight=1)
    tk_widgets.WT.action3_frame.columnconfigure(2, weight=1)
    tk_widgets.WT.action3_frame.columnconfigure(3, weight=10)
    tk_widgets.WT.action3_frame.columnconfigure(4, weight=10)

    def add_cmd(wad_paths):
        def add_thrd():
            LOG('wad_tool: Running: Load WADs.')
            hash_manager.read_wad_hashes()
            for wad_path in wad_paths:
                try:
                    wad = pyRitoFile.read_wad(wad_path)
                    wad.un_hash(hash_manager.HASHTABLES)
                    tk_widgets.WT.loaded_wads.append(wad)
                    tk_widgets.WT.loaded_wad_paths.append(wad_path)
                    tk_widgets.WT.loaded_chunk_hashes.extend(
                        chunk.hash for chunk in wad.chunks)
                except:
                    pass
            hash_manager.free_wad_hashes()
            LOG('wad_tool: Done: Load WADs.')
            tk_widgets.WT.wad_text.configure(state=tk.NORMAL)
            tk_widgets.WT.wad_text.insert(
                tk.END, '\n'.join(tk_widgets.WT.loaded_wad_paths) + '\n')
            tk_widgets.WT.wad_text.configure(state=tk.DISABLED)
            tk_widgets.WT.chunk_text.configure(state=tk.NORMAL)
            tk_widgets.WT.chunk_text.insert(
                tk.END, '\n'.join(tk_widgets.WT.loaded_chunk_hashes) + '\n')
            tk_widgets.WT.chunk_text.configure(state=tk.DISABLED)

        if check_thread_safe(tk_widgets.WT.working_thread):
            tk_widgets.WT.working_thread = Thread(target=add_thrd, daemon=True)
            tk_widgets.WT.working_thread.start()
        else:
            LOG(
                'wad_tool: Failed: A thread is already running, wait for it to finished.')

    def addfile_cmd():
        file_paths = tkfd.askopenfilenames(
            parent=tk_widgets.main_tk,
            title='Select WADs',
            filetypes=(
                ('WAD files', '*.wad.client'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        if len(file_paths) > 0:
            add_cmd(file_paths)

    # create add file button
    tk_widgets.WT.addfile_button = ctk.CTkButton(
        tk_widgets.WT.action3_frame,
        text='Add WADs',
        image=EmojiImage.create('📦'),
        command=addfile_cmd,
        font=le_font
    )
    tk_widgets.WT.addfile_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def addfolder_cmd():
        dirname = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select Folder contains WADs',
            initialdir=setting.get('default_folder', None)
        )
        file_paths = []
        for root, dirs, files in os.walk(dirname):
            for file in files:
                if file.endswith('.wad.client'):
                    file_paths.append(os.path.join(
                        root, file).replace('\\', '/'))
        if len(file_paths) > 0:
            add_cmd(file_paths)

    # create add folder button
    tk_widgets.WT.addfolder_button = ctk.CTkButton(
        tk_widgets.WT.action3_frame,
        text='Scan WADs in folder',
        image=EmojiImage.create('📁'),
        command=addfolder_cmd,
        font=le_font
    )
    tk_widgets.WT.addfolder_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def clear_cmd():
        tk_widgets.WT.loaded_wads = []
        tk_widgets.WT.loaded_wad_paths = []
        tk_widgets.WT.loaded_chunk_hashes = []
        tk_widgets.WT.wad_text.configure(state=tk.NORMAL)
        tk_widgets.WT.wad_text.delete('1.0', tk.END)
        tk_widgets.WT.wad_text.configure(state=tk.DISABLED)
        tk_widgets.WT.chunk_text.configure(state=tk.NORMAL)
        tk_widgets.WT.chunk_text.delete('1.0', tk.END)
        tk_widgets.WT.chunk_text.configure(state=tk.DISABLED)

    # create clear button
    tk_widgets.WT.clear_button = ctk.CTkButton(
        tk_widgets.WT.action3_frame,
        text='Clear',
        image=EmojiImage.create('❌'),
        command=clear_cmd,
        font=le_font
    )
    tk_widgets.WT.clear_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

    # filter command for both include and exclude entry
    def filter_cmd(event):
        # get keywords
        include_keywords = tk_widgets.WT.include_entry.get().split()
        exclude_keywords = tk_widgets.WT.exclude_entry.get().split()
        if len(include_keywords) == 0:
            # reset include
            tk_widgets.WT.chunk_text.tag_remove('include', '1.0', tk.END)
            tk_widgets.WT.chunk_text.configure(state=tk.NORMAL)
            tk_widgets.WT.chunk_text.delete('1.0', tk.END)
            tk_widgets.WT.chunk_text.insert(
                tk.END, '\n'.join(tk_widgets.WT.loaded_chunk_hashes) + '\n')
            tk_widgets.WT.chunk_text.configure(state=tk.DISABLED)
            return
        # filter inside core first
        temp_chunk_hashes = []
        for chunk_hash in tk_widgets.WT.loaded_chunk_hashes:
            allow = True
            for keyword in include_keywords:
                if keyword not in chunk_hash:
                    allow = False
                    break
            for keyword in exclude_keywords:
                if keyword in chunk_hash:
                    allow = False
                    break
            if allow:
                temp_chunk_hashes.append(chunk_hash)

        # reset tk text with filtered core
        if len(temp_chunk_hashes) != len(tk_widgets.WT.loaded_chunk_hashes):
            tk_widgets.WT.chunk_text.configure(state=tk.NORMAL)
            tk_widgets.WT.chunk_text.delete('1.0', tk.END)
            tk_widgets.WT.chunk_text.insert(
                tk.END, '\n'.join(temp_chunk_hashes) + '\n')
            tk_widgets.WT.chunk_text.configure(state=tk.DISABLED)

        # hightlight tk text
        tk_widgets.WT.chunk_text.tag_remove('include', '1.0', tk.END)
        tk_widgets.WT.chunk_text.tag_config(
            'include', foreground=tk_widgets.c_active_fg[0])
        for keyword in include_keywords:
            start_index = '1.0'
            keyword_length = len(keyword)
            while True:
                start_index = tk_widgets.WT.chunk_text.search(
                    keyword,
                    start_index,
                    nocase=True,
                    stopindex=tk.END
                )
                if start_index == '':
                    break
                end_index = f'{start_index} + {keyword_length}c'
                tk_widgets.WT.chunk_text.tag_add(
                    'include', start_index, end_index)
                start_index = end_index

    # create include entry
    tk_widgets.WT.include_entry = ctk.CTkEntry(
        tk_widgets.WT.action3_frame,
        placeholder_text='Include keywords',
        font=le_font
    )
    tk_widgets.WT.include_entry.grid(
        row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.WT.include_entry.bind('<Return>', filter_cmd)

    # create exclude entry
    tk_widgets.WT.exclude_entry = ctk.CTkEntry(
        tk_widgets.WT.action3_frame,
        placeholder_text='Exclude keywords (after include)',
        font=le_font
    )
    tk_widgets.WT.exclude_entry.grid(
        row=0, column=4, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.WT.exclude_entry.bind('<Return>', filter_cmd)

    # create label frame
    tk_widgets.WT.label_frame = ctk.CTkFrame(
        tk_widgets.WT.action2_frame
    )
    tk_widgets.WT.label_frame.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.WT.label_frame.rowconfigure(0, weight=1)
    tk_widgets.WT.label_frame.columnconfigure(0, weight=3)
    tk_widgets.WT.label_frame.columnconfigure(1, weight=7)
    # create wad text
    tk_widgets.WT.wad_text = ctk.CTkTextbox(
        tk_widgets.WT.label_frame,
        wrap=tk.NONE,
        state=tk.DISABLED,
        font=le_font
    )
    tk_widgets.WT.wad_text.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create chunk text
    tk_widgets.WT.chunk_text = ctk.CTkTextbox(
        tk_widgets.WT.label_frame,
        wrap=tk.NONE,
        state=tk.DISABLED,
        font=le_font
    )
    tk_widgets.WT.chunk_text.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def bulk_cmd():
        if check_thread_safe(tk_widgets.WT.working_thread):
            dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Output Folder',
                initialdir=setting.get('default_folder', None)
            )
            if dir_path != '':
                wad_paths = tk_widgets.WT.wad_text.get(
                    '1.0', 'end-1c').split('\n')
                chunk_hashes = tk_widgets.WT.chunk_text.get(
                    '1.0', 'end-1c').split('\n')
                if len(chunk_hashes) == 0:
                    chunk_hashes = None
                wad_paths.remove('')
                if len(wad_paths) > 0:
                    def working_thrd():
                        hash_manager.read_wad_hashes()
                        Log.tk_cooldown = 5000
                        for wad_path in wad_paths:
                            wad_tool.unpack(wad_path, dir_path,
                                            hash_manager.HASHTABLES, filter=chunk_hashes)
                        Log.tk_cooldown = 0
                        hash_manager.free_wad_hashes()
                        LOG(f'wad_tool: Done: Unpack to {dir_path}')
                    tk_widgets.WT.working_thread = Thread(
                        target=working_thrd, daemon=True)
                    tk_widgets.WT.working_thread.start()
        else:
            LOG(
                'wad_tool: Failed: A thread is already running, wait for it to finished.')
    # create bulk button
    tk_widgets.WT.bulk_button = ctk.CTkButton(
        tk_widgets.WT.action2_frame,
        text='Bulk Unpack',
        image=EmojiImage.create('⏏️', weird=True),
        command=bulk_cmd,
        font=le_font
    )
    tk_widgets.WT.bulk_button.grid(
        row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)


def create_PT_page():
    # create page frame
    tk_widgets.PT.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.PT.page_frame.columnconfigure(0, weight=1)
    tk_widgets.PT.page_frame.rowconfigure(0, weight=1)
    tk_widgets.PT.page_frame.rowconfigure(1, weight=699)
    # handle drop in PT
    def page_drop_cmd(event):
        def page_drop_thrd():
            paths = dnd_return_handle(event.data)
            for path in paths:
                path = path.replace('\\', '/')
                pyntex.parse(path)
        if check_thread_safe(tk_widgets.PT.working_thread):
            tk_widgets.PT.working_thread = Thread(
                target=page_drop_thrd,
                daemon=True
            )
            tk_widgets.PT.working_thread.start()
        else:
            LOG('wad_tool: Failed: A thread is already running, wait for it to finished.')
    tk_widgets.PT.page_frame.drop_target_register(tkdnd.DND_FILES)
    tk_widgets.PT.page_frame.dnd_bind('<<Drop>>', page_drop_cmd)
    # init stuffs
    tk_widgets.PT.working_thread = None
    # create action frame
    tk_widgets.PT.action_frame = ctk.CTkFrame(
        tk_widgets.PT.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.PT.action_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.PT.action_frame.rowconfigure(0, weight=1)
    tk_widgets.PT.action_frame.columnconfigure(0, weight=1)
    tk_widgets.PT.action_frame.columnconfigure(1, weight=1)
    tk_widgets.PT.action_frame.columnconfigure(2, weight=699)

    def parsewad_cmd():
        if check_thread_safe(tk_widgets.PT.working_thread):
            file_paths = tkfd.askopenfilenames(
                parent=tk_widgets.main_tk,
                title='Select WADs',
                filetypes=(
                    ('WAD files', '*.wad.client'),
                    ('All files', '*.*'),
                ),
                initialdir=setting.get('default_folder', None)
            )
            if len(file_paths) > 0:
                def working_thrd():
                    for file_path in file_paths:
                        pyntex.parse(file_path)
                tk_widgets.PT.working_thread = Thread(
                    target=working_thrd,
                    daemon=True
                )
                tk_widgets.PT.working_thread.start()
        else:
            LOG(
                'pyntex: Failed: A thread is already running, wait for it to finished.')
    # create parse wad button
    tk_widgets.PT.parsewad_button = ctk.CTkButton(
        tk_widgets.PT.action_frame,
        text='Parse WAD',
        image=EmojiImage.create('📦'),
        anchor=tk.CENTER,
        command=parsewad_cmd,
        font=le_font
    )
    tk_widgets.PT.parsewad_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def parsedir_cmd():
        if check_thread_safe(tk_widgets.PT.working_thread):
            dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Folder',
                initialdir=setting.get('default_folder', None)
            )
            if dir_path != '':
                def working_thrd():
                    pyntex.parse(dir_path)
                tk_widgets.PT.working_thread = Thread(
                    target=working_thrd,
                    daemon=True
                )
                tk_widgets.PT.working_thread.start()
        else:
            LOG(
                'pyntex: Failed: A thread is already running, wait for it to finished.')
    # create parse folder button
    tk_widgets.PT.parsedir_button = ctk.CTkButton(
        tk_widgets.PT.action_frame,
        text='Parse Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=parsedir_cmd,
        font=le_font
    )
    tk_widgets.PT.parsedir_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)


def create_LOG_page():
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
        wrap=tk.WORD,
        state=tk.DISABLED,
        border_spacing=10,
        font=le_font
    )
    tk_widgets.LOG.log_textbox.grid(row=0, column=0, sticky=tk.NSEW)
    Log.tk_log = tk_widgets.LOG.log_textbox


def create_SBORF_page():
    tk_widgets.SBORF.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.SBORF.page_frame.columnconfigure(0, weight=1)
    tk_widgets.SBORF.page_frame.rowconfigure(0, weight=1)
    tk_widgets.SBORF.page_frame.rowconfigure(1, weight=1)
    tk_widgets.SBORF.page_frame.rowconfigure(2, weight=999)

    # create action frame
    tk_widgets.SBORF.action_frame = ctk.CTkFrame(
        tk_widgets.SBORF.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.SBORF.action_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SBORF.action_frame.columnconfigure(0, weight=999)
    tk_widgets.SBORF.action_frame.columnconfigure(1, weight=1)
    tk_widgets.SBORF.action_frame.rowconfigure(0, weight=1)

    def backup_cmd():
        setting.set('Sborf.backup', tk_widgets.SBORF.backup_switch.get())
        setting.save()
    # create backup switch
    tk_widgets.SBORF.backup_switch = ctk.CTkSwitch(
        tk_widgets.SBORF.action_frame,
        text='Create backup before fix (safe)',
        command=backup_cmd,
        font=le_font
    )
    if setting.get('Sborf.backup', 1) == 1:
        tk_widgets.SBORF.backup_switch.select()
    else:
        tk_widgets.SBORF.backup_switch.deselect()
    tk_widgets.SBORF.backup_switch.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create skin frame
    tk_widgets.SBORF.skin_frame = ctk.CTkFrame(
        tk_widgets.SBORF.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.SBORF.skin_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SBORF.skin_frame.rowconfigure(0, weight=5)
    tk_widgets.SBORF.skin_frame.rowconfigure(1, weight=5)
    tk_widgets.SBORF.skin_frame.columnconfigure(0, weight=1)

    # create browse frame
    tk_widgets.SBORF.browse_frame = ctk.CTkFrame(
        tk_widgets.SBORF.skin_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.SBORF.browse_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SBORF.browse_frame.rowconfigure(0, weight=1)
    tk_widgets.SBORF.browse_frame.rowconfigure(1, weight=1)
    tk_widgets.SBORF.browse_frame.rowconfigure(2, weight=1)
    tk_widgets.SBORF.browse_frame.rowconfigure(3, weight=1)
    tk_widgets.SBORF.browse_frame.rowconfigure(4, weight=999)
    tk_widgets.SBORF.browse_frame.columnconfigure(0, weight=20)
    tk_widgets.SBORF.browse_frame.columnconfigure(1, weight=1)
    tk_widgets.SBORF.browse_frame.columnconfigure(2, weight=20)
    tk_widgets.SBORF.browse_frame.columnconfigure(3, weight=1)

    # create your skin label
    tk_widgets.SBORF.yourskin_label = ctk.CTkLabel(
        tk_widgets.SBORF.browse_frame,
        text='Your skin',
        anchor=tk.CENTER,
        justify=tk.CENTER,
        font=le_font
    )
    tk_widgets.SBORF.yourskin_label.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    # create riot skin label
    tk_widgets.SBORF.riotskin_label = ctk.CTkLabel(
        tk_widgets.SBORF.browse_frame,
        text='Rito skin',
        anchor=tk.CENTER,
        justify=tk.CENTER,
        font=le_font
    )
    tk_widgets.SBORF.riotskin_label.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

    # create skl entry
    tk_widgets.SBORF.skl_entry = ctk.CTkEntry(
        tk_widgets.SBORF.browse_frame,
        placeholder_text='(Require)',
        font=le_font
    )
    tk_widgets.SBORF.skl_entry.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def sklbrowse_cmd():
        skl_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select your SKL file',
            filetypes=(
                ('SKL files', '*.skl'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.SBORF.skl_entry.delete(0, tk.END)
        tk_widgets.SBORF.skl_entry.insert(tk.END, skl_path)
        skn_path = skl_path.replace('.skl', '.skn')
        if os.path.exists(skn_path) and tk_widgets.SBORF.skn_entry.get() == '':
            tk_widgets.SBORF.skn_entry.delete(0, tk.END)
            tk_widgets.SBORF.skn_entry.insert(tk.END, skn_path)

    # create skl browse button
    tk_widgets.SBORF.sklbrowse_button = ctk.CTkButton(
        tk_widgets.SBORF.browse_frame,
        text='Browse SKL',
        image=EmojiImage.create('🦴'),
        anchor=tk.CENTER,
        command=sklbrowse_cmd,
        font=le_font
    )
    tk_widgets.SBORF.sklbrowse_button.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create riot skl entry
    tk_widgets.SBORF.riotskl_entry = ctk.CTkEntry(
        tk_widgets.SBORF.browse_frame,
        placeholder_text='(Require)',
        font=le_font
    )
    tk_widgets.SBORF.riotskl_entry.grid(
        row=1, column=2, padx=5, pady=5, sticky=tk.NSEW)

    def riotsklbrowse_cmd():
        skl_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select riot SKL file',
            filetypes=(
                ('SKL files', '*.skl'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.SBORF.riotskl_entry.delete(0, tk.END)
        tk_widgets.SBORF.riotskl_entry.insert(tk.END, skl_path)
    # create riot skl browse button
    tk_widgets.SBORF.riotsklbrowse_button = ctk.CTkButton(
        tk_widgets.SBORF.browse_frame,
        text='Browse Riot SKL',
        image=EmojiImage.create('🦴'),
        anchor=tk.CENTER,
        command=riotsklbrowse_cmd,
        font=le_font
    )
    tk_widgets.SBORF.riotsklbrowse_button.grid(
        row=1, column=3, padx=5, pady=5, sticky=tk.NSEW)

    # create skn entry
    tk_widgets.SBORF.skn_entry = ctk.CTkEntry(
        tk_widgets.SBORF.browse_frame,
        placeholder_text='(Require if fix skin)',
        font=le_font
    )
    tk_widgets.SBORF.skn_entry.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def sknbrowse_cmd():
        skn_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select your SKN file',
            filetypes=(
                ('SKN files', '*.skn'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.SBORF.skn_entry.delete(0, tk.END)
        tk_widgets.SBORF.skn_entry.insert(tk.END, skn_path)
        skl_path = os.path.join(
            os.path.dirname(skn_path), os.path.basename(skn_path).replace('.skn', '') + '.skl').replace('\\', '/')
        if os.path.exists(skl_path) and tk_widgets.SBORF.skl_entry.get() == '':
            tk_widgets.SBORF.skl_entry.delete(0, tk.END)
            tk_widgets.SBORF.skl_entry.insert(tk.END, skl_path)
    # create skn browse button
    tk_widgets.SBORF.sknbrowse_button = ctk.CTkButton(
        tk_widgets.SBORF.browse_frame,
        text='Browse SKN',
        image=EmojiImage.create('🧊'),
        anchor=tk.CENTER,
        command=sknbrowse_cmd,
        font=le_font
    )
    tk_widgets.SBORF.sknbrowse_button.grid(
        row=2, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create riot skn entry
    tk_widgets.SBORF.riotskn_entry = ctk.CTkEntry(
        tk_widgets.SBORF.browse_frame,
        placeholder_text='(Leave empty if dont need)',
        font=le_font
    )
    tk_widgets.SBORF.riotskn_entry.grid(
        row=2, column=2, padx=5, pady=5, sticky=tk.NSEW)

    def riotsknbrowse_cmd():
        skn_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select riot SKN file',
            filetypes=(
                ('SKN files', '*.skn'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.SBORF.riotskn_entry.delete(0, tk.END)
        tk_widgets.SBORF.riotskn_entry.insert(tk.END, skn_path)
    # create riot skn browse button
    tk_widgets.SBORF.riotsknbrowse_button = ctk.CTkButton(
        tk_widgets.SBORF.browse_frame,
        text='Browse Riot SKN',
        image=EmojiImage.create('🧊'),
        anchor=tk.CENTER,
        command=riotsknbrowse_cmd,
        font=le_font
    )
    tk_widgets.SBORF.riotsknbrowse_button.grid(
        row=2, column=3, padx=5, pady=5, sticky=tk.NSEW)

    # create bin entry
    tk_widgets.SBORF.bin_entry = ctk.CTkEntry(
        tk_widgets.SBORF.browse_frame,
        placeholder_text='(Require if adapt MaskData)',
        font=le_font
    )
    tk_widgets.SBORF.bin_entry.grid(
        row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def binbrowse_cmd():
        bin_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select your Animation BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.SBORF.bin_entry.delete(0, tk.END)
        tk_widgets.SBORF.bin_entry.insert(tk.END, bin_path)
    # create bin browse button
    tk_widgets.SBORF.binbrowse_button = ctk.CTkButton(
        tk_widgets.SBORF.browse_frame,
        text='Browse Animation BIN',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=binbrowse_cmd,
        font=le_font
    )
    tk_widgets.SBORF.binbrowse_button.grid(
        row=3, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create riot bin entry
    tk_widgets.SBORF.riotbin_entry = ctk.CTkEntry(
        tk_widgets.SBORF.browse_frame,
        placeholder_text='(Require if adapt MaskData)',
        font=le_font
    )
    tk_widgets.SBORF.riotbin_entry.grid(
        row=3, column=2, padx=5, pady=5, sticky=tk.NSEW)

    def riotbinbrowse_cmd():
        bin_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select Riot Animtion BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.SBORF.riotbin_entry.delete(0, tk.END)
        tk_widgets.SBORF.riotbin_entry.insert(tk.END, bin_path)
    # create riot bin browse button
    tk_widgets.SBORF.riotbinbrowse_button = ctk.CTkButton(
        tk_widgets.SBORF.browse_frame,
        text='Browse Riot Animtion BIN',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=riotbinbrowse_cmd,
        font=le_font
    )
    tk_widgets.SBORF.riotbinbrowse_button.grid(
        row=3, column=3, padx=5, pady=5, sticky=tk.NSEW)

    # create skin frame
    tk_widgets.SBORF.fix_frame = ctk.CTkFrame(
        tk_widgets.SBORF.skin_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.SBORF.fix_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SBORF.fix_frame.columnconfigure(0, weight=1)
    tk_widgets.SBORF.fix_frame.columnconfigure(1, weight=999)
    tk_widgets.SBORF.fix_frame.rowconfigure(0, weight=1)
    tk_widgets.SBORF.fix_frame.rowconfigure(1, weight=1)
    tk_widgets.SBORF.fix_frame.rowconfigure(2, weight=1)
    tk_widgets.SBORF.fix_frame.rowconfigure(4, weight=1)
    tk_widgets.SBORF.fix_frame.rowconfigure(5, weight=1)
    tk_widgets.SBORF.fix_frame.rowconfigure(6, weight=1)
    tk_widgets.SBORF.fix_frame.rowconfigure(7, weight=999)

    def skinfix_cmd(dont_add_joint_back=False):
        skl_path = tk_widgets.SBORF.skl_entry.get()
        if skl_path == '':
            raise Exception('sborf: Failed: Read SKL: Empty path.')
        skn_path = tk_widgets.SBORF.skn_entry.get()
        if skn_path == '':
            raise Exception('sborf: Failed: Read SKN: Empty path.')
        riotskl_path = tk_widgets.SBORF.riotskl_entry.get()
        if riotskl_path == '':
            raise Exception(
                'sborf: Failed: Read Riot SKL: Empty Riot path.')
        riotskn_path = tk_widgets.SBORF.riotskn_entry.get()
        sborf.skin_fix(skl_path, skn_path, riotskl_path, riotskn_path,
                       backup=setting.get('Sborf.backup', 1), dont_add_joint_back=dont_add_joint_back)

    def adaptmaskdata_cmd():
        skl_path = tk_widgets.SBORF.skl_entry.get()
        if skl_path == '':
            raise Exception('sborf: Failed: Read SKL: Empty path.')
        bin_path = tk_widgets.SBORF.bin_entry.get()
        if bin_path == '':
            raise Exception('sborf: Failed: Read Animation BIN: Empty path.')
        riotskl_path = tk_widgets.SBORF.riotskl_entry.get()
        if riotskl_path == '':
            raise Exception(
                'sborf: Failed: Read Riot SKL: Empty path.')
        riotbin_path = tk_widgets.SBORF.riotbin_entry.get()
        if riotbin_path == '':
            raise Exception(
                'sborf: Failed: Read Riot Animation BIN: Empty path.')
        sborf.maskdata_adapt(skl_path, riotskl_path, bin_path, riotbin_path,
                             backup=setting.get('Sborf.backup', 1))

    # create fixskin button
    tk_widgets.SBORF.fixskin_button = ctk.CTkButton(
        tk_widgets.SBORF.fix_frame,
        text='Fix your skin',
        image=EmojiImage.create('🐊'),
        anchor=tk.CENTER,
        command=skinfix_cmd,
        font=le_font
    )
    tk_widgets.SBORF.fixskin_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SBORF.fixskin_label = ctk.CTkLabel(
        tk_widgets.SBORF.fix_frame,
        text='Sort your SKL joints base on riot SKL, fill removed riot joints back and move new custom joints to the end of list.\nSort SKN vertex influences base on the new order.\nIf selected riot SKN, sort SKN materials base on riot SKN.\nThrow exception if total joints = your SKL joints + removed joints > 256.',
        anchor=tk.NW,
        justify=tk.LEFT,
        font=le_font
    )
    tk_widgets.SBORF.fixskin_label.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create fixskin2 button
    tk_widgets.SBORF.fixskin2_button = ctk.CTkButton(
        tk_widgets.SBORF.fix_frame,
        text='Fix your skin but do not add removed riot joint back',
        image=EmojiImage.create('🐸'),
        anchor=tk.CENTER,
        command=lambda: skinfix_cmd(dont_add_joint_back=True),
        font=le_font
    )
    tk_widgets.SBORF.fixskin2_button.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SBORF.fixskin2_label = ctk.CTkLabel(
        tk_widgets.SBORF.fix_frame,
        text='Sort your custom SKL joints order similar to riot SKL and your new joints also moved to the end of list.\nYou need to use custom animation BIN MaskData tho.',
        anchor=tk.NW,
        justify=tk.LEFT,
        font=le_font
    )
    tk_widgets.SBORF.fixskin2_label.grid(
        row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create adaptmaskdata button
    tk_widgets.SBORF.adaptmaskdata_button = ctk.CTkButton(
        tk_widgets.SBORF.fix_frame,
        text='Adapt animation BIN MaskData',
        image=EmojiImage.create('🦀'),
        anchor=tk.CENTER,
        command=adaptmaskdata_cmd,
        font=le_font
    )
    tk_widgets.SBORF.adaptmaskdata_button.grid(
        row=4, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.SBORF.adaptmaskdata_label = ctk.CTkLabel(
        tk_widgets.SBORF.fix_frame,
        text='Copy MaskData weight values from riot animation BIN to your custom animation BIN base on your SKL+riot SKL.\nNew custom joints will have weight set to 0.0.',
        anchor=tk.NW,
        justify=tk.LEFT,
        font=le_font
    )
    tk_widgets.SBORF.adaptmaskdata_label.grid(
        row=5, column=0, padx=5, pady=5, sticky=tk.NSEW)


def create_LOLFBX_page():
    tk_widgets.LOLFBX.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.LOLFBX.page_frame.columnconfigure(0, weight=1)
    tk_widgets.LOLFBX.page_frame.rowconfigure(0, weight=1)
    tk_widgets.LOLFBX.page_frame.rowconfigure(1, weight=999)

    def page_drop_cmd(event):
        path = dnd_return_handle(event.data)[0]
        if path.endswith('.skl'):
            skl_path = path
            skn_path = path.replace('.skl', '.skn')
            fbx_path = path.replace('.skl', '.fbx')
            tk_widgets.LOLFBX.skl_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.skl_entry.insert(tk.END, skl_path)
            if tk_widgets.LOLFBX.skn_entry.get() == '':
                tk_widgets.LOLFBX.skn_entry.delete(0, tk.END)
                tk_widgets.LOLFBX.skn_entry.insert(tk.END, skn_path)
            if tk_widgets.LOLFBX.fbx_entry.get() == '':
                tk_widgets.LOLFBX.fbx_entry.delete(0, tk.END)
                tk_widgets.LOLFBX.fbx_entry.insert(tk.END, fbx_path)
        elif path.endswith('.skn'):
            skn_path = path
            skl_path = path.replace('.skn', '.skl')
            fbx_path = path.replace('.skn', '.fbx')
            tk_widgets.LOLFBX.skn_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.skn_entry.insert(tk.END, skn_path)
            if tk_widgets.LOLFBX.skl_entry.get() == '':
                tk_widgets.LOLFBX.skl_entry.delete(0, tk.END)
                tk_widgets.LOLFBX.skl_entry.insert(tk.END, skl_path)
            if tk_widgets.LOLFBX.fbx_entry.get() == '':
                tk_widgets.LOLFBX.fbx_entry.delete(0, tk.END)
                tk_widgets.LOLFBX.fbx_entry.insert(tk.END, fbx_path)
        elif path.endswith('.fbx'):
            fbx_path = path
            skn_path = path.replace('.fbx', '.skn')
            skl_path = path.replace('.fbx', '.skl')
            tk_widgets.LOLFBX.fbx_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.fbx_entry.insert(tk.END, fbx_path)
            if tk_widgets.LOLFBX.skn_entry.get() == '':
                tk_widgets.LOLFBX.skn_entry.delete(0, tk.END)
                tk_widgets.LOLFBX.skn_entry.insert(tk.END, skn_path)
            if tk_widgets.LOLFBX.skl_entry.get() == '':
                tk_widgets.LOLFBX.skl_entry.delete(0, tk.END)
                tk_widgets.LOLFBX.skl_entry.insert(tk.END, skl_path)

    tk_widgets.LOLFBX.page_frame.drop_target_register(
        tkdnd.DND_FILES)
    tk_widgets.LOLFBX.page_frame.dnd_bind(
        '<<Drop>>', page_drop_cmd)

    # create skin frame
    tk_widgets.LOLFBX.skin_frame = ctk.CTkFrame(
        tk_widgets.LOLFBX.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.LOLFBX.skin_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.LOLFBX.skin_frame.rowconfigure(0, weight=2)
    tk_widgets.LOLFBX.skin_frame.rowconfigure(1, weight=8)
    tk_widgets.LOLFBX.skin_frame.rowconfigure(2, weight=2)
    tk_widgets.LOLFBX.skin_frame.columnconfigure(0, weight=1)
    # create tool label 1
    tk_widgets.LOLFBX.tool_label1 = ctk.CTkLabel(
        tk_widgets.LOLFBX.skin_frame,
        text = 'FBX <-> SKIN',
        font=le_font
    )
    tk_widgets.LOLFBX.tool_label1.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    # create browse frame
    tk_widgets.LOLFBX.browse_frame = ctk.CTkFrame(
        tk_widgets.LOLFBX.skin_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.LOLFBX.browse_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.LOLFBX.browse_frame.rowconfigure(0, weight=1)
    tk_widgets.LOLFBX.browse_frame.rowconfigure(1, weight=1)
    tk_widgets.LOLFBX.browse_frame.rowconfigure(2, weight=1)
    tk_widgets.LOLFBX.browse_frame.rowconfigure(3, weight=999)
    tk_widgets.LOLFBX.browse_frame.columnconfigure(0, weight=9)
    tk_widgets.LOLFBX.browse_frame.columnconfigure(1, weight=1)

    # create fbx entry
    tk_widgets.LOLFBX.fbx_entry = ctk.CTkEntry(
        tk_widgets.LOLFBX.browse_frame,
        font=le_font
    )
    tk_widgets.LOLFBX.fbx_entry.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    def fbxbrowse_cmd():
        fbx_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select your FBX file',
            filetypes=(
                ('FBX files', '*.fbx'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.LOLFBX.fbx_entry.delete(0, tk.END)
        tk_widgets.LOLFBX.fbx_entry.insert(tk.END, fbx_path)
        skn_path = fbx_path.replace('.fbx', '.skn')
        if tk_widgets.LOLFBX.skn_entry.get() == '':
            tk_widgets.LOLFBX.skn_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.skn_entry.insert(tk.END, skn_path)
        skl_path = fbx_path.replace('.fbx', '.skl')
        if tk_widgets.LOLFBX.skl_entry.get() == '':
            tk_widgets.LOLFBX.skl_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.skl_entry.insert(tk.END, skl_path)
    # create fbx browse button
    tk_widgets.LOLFBX.fbxbrowse_button = ctk.CTkButton(
        tk_widgets.LOLFBX.browse_frame,
        text='Browse FBX',
        image=EmojiImage.create('🌄'),
        anchor=tk.CENTER,
        command=fbxbrowse_cmd,
        font=le_font
    )
    tk_widgets.LOLFBX.fbxbrowse_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create skl entry
    tk_widgets.LOLFBX.skl_entry = ctk.CTkEntry(
        tk_widgets.LOLFBX.browse_frame,
        font=le_font
    )
    tk_widgets.LOLFBX.skl_entry.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    def sklbrowse_cmd():
        skl_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select your SKL file',
            filetypes=(
                ('SKL files', '*.skl'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.LOLFBX.skl_entry.delete(0, tk.END)
        tk_widgets.LOLFBX.skl_entry.insert(tk.END, skl_path)
        fbx_path = skl_path.replace('.skl', '.fbx')
        if tk_widgets.LOLFBX.fbx_entry.get() == '':
            tk_widgets.LOLFBX.fbx_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.fbx_entry.insert(tk.END, fbx_path)
        skn_path = skl_path.replace('.skl', '.skn')
        if tk_widgets.LOLFBX.skn_entry.get() == '':
            tk_widgets.LOLFBX.skn_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.skn_entry.insert(tk.END, skn_path)
        
    # create skl browse button
    tk_widgets.LOLFBX.sklbrowse_button = ctk.CTkButton(
        tk_widgets.LOLFBX.browse_frame,
        text='Browse SKL',
        image=EmojiImage.create('🦴'),
        anchor=tk.CENTER,
        command=sklbrowse_cmd,
        font=le_font
    )
    tk_widgets.LOLFBX.sklbrowse_button.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create skn entry
    tk_widgets.LOLFBX.skn_entry = ctk.CTkEntry(
        tk_widgets.LOLFBX.browse_frame,
        font=le_font
    )
    tk_widgets.LOLFBX.skn_entry.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    def sknbrowse_cmd():
        skn_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select your SKN file',
            filetypes=(
                ('SKN files', '*.skn'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.LOLFBX.skn_entry.delete(0, tk.END)
        tk_widgets.LOLFBX.skn_entry.insert(tk.END, skn_path)
        fbx_path = skn_path.replace('.skn', '.fbx')
        if tk_widgets.LOLFBX.fbx_entry.get() == '':
            tk_widgets.LOLFBX.fbx_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.fbx_entry.insert(tk.END, fbx_path)
        skl_path = skn_path.replace('.skn', '.skl')
        if tk_widgets.LOLFBX.skl_entry.get() == '':
            tk_widgets.LOLFBX.skl_entry.delete(0, tk.END)
            tk_widgets.LOLFBX.skl_entry.insert(tk.END, skl_path)
    # create fbx browse button
    tk_widgets.LOLFBX.sknbrowse_button = ctk.CTkButton(
        tk_widgets.LOLFBX.browse_frame,
        text='Browse SKN',
        image=EmojiImage.create('🧊'),
        anchor=tk.CENTER,
        command=sknbrowse_cmd,
        font=le_font
    )
    tk_widgets.LOLFBX.sknbrowse_button.grid(
        row=2, column=1, padx=5, pady=5, sticky=tk.NSEW)
    
    # create action frame
    tk_widgets.LOLFBX.action_frame = ctk.CTkFrame(
        tk_widgets.LOLFBX.skin_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.LOLFBX.action_frame.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.LOLFBX.action_frame.rowconfigure(0, weight=0)
    tk_widgets.LOLFBX.action_frame.columnconfigure(0, weight=2)
    tk_widgets.LOLFBX.action_frame.columnconfigure(1, weight=6)
    tk_widgets.LOLFBX.action_frame.columnconfigure(2, weight=2)

    def fbx2skin_cmd():
        lol2fbx.fbx_to_skin(
            fbx_path=tk_widgets.LOLFBX.fbx_entry.get(),
            skl_path=tk_widgets.LOLFBX.skl_entry.get(),
            skn_path=tk_widgets.LOLFBX.skn_entry.get()
        )

    # create fbx2skin button
    tk_widgets.LOLFBX.fbx2skin_button = ctk.CTkButton(
        tk_widgets.LOLFBX.action_frame,
        text='FBX -> SKIN',
        image=EmojiImage.create('🛸'),
        anchor=tk.CENTER,
        command=fbx2skin_cmd,
        font=le_font
    )
    tk_widgets.LOLFBX.fbx2skin_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    def skin2fbx_cmd():
        lol2fbx.skin_to_fbx(
            skl_path=tk_widgets.LOLFBX.skl_entry.get(),
            skn_path=tk_widgets.LOLFBX.skn_entry.get(),
            fbx_path=tk_widgets.LOLFBX.fbx_entry.get()
        )

    # create skin2fbx button
    tk_widgets.LOLFBX.skin2fbx_button = ctk.CTkButton(
        tk_widgets.LOLFBX.action_frame,
        text='SKIN -> FBX',
        image=EmojiImage.create('👽'),
        anchor=tk.CENTER,
        command=skin2fbx_cmd,
        font=le_font
    )
    tk_widgets.LOLFBX.skin2fbx_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

def create_BNKT_page():
    # apply style to ttk treeview
    bg_color = tk_widgets.main_tk._apply_appearance_mode(ctk.ThemeManager.theme['CTkFrame']['fg_color'])
    text_color = tk_widgets.main_tk._apply_appearance_mode(ctk.ThemeManager.theme['CTkLabel']['text_color'])
    selected_color = tk_widgets.main_tk._apply_appearance_mode(ctk.ThemeManager.theme['CTkButton']['fg_color'])
    font = ctk.CTkLabel(None).cget('font')
    font_size = font.cget('size')
    font.configure(size=int(font_size*1.4))
    treestyle = ttk.Style()
    treestyle.theme_use('default')
    treestyle.configure('Treeview', background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0, font=font, rowheight=int(font_size*2.5))
    treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
    tk_widgets.main_tk.bind('<<TreeviewSelect>>', lambda event: tk_widgets.main_tk.focus_set())
    
    tk_widgets.BNKT.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.BNKT.page_frame.columnconfigure(0, weight=1)
    tk_widgets.BNKT.page_frame.rowconfigure(0, weight=1)
    tk_widgets.BNKT.page_frame.rowconfigure(1, weight=999)

    # init stuffs
    tk_widgets.BNKT.treeview = None
    tk_widgets.BNKT.working_thread = None

    # create input frame
    tk_widgets.BNKT.input_frame = ctk.CTkFrame(
        tk_widgets.BNKT.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.BNKT.input_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.BNKT.input_frame.columnconfigure(0, weight=9)
    tk_widgets.BNKT.input_frame.columnconfigure(1, weight=1)
    tk_widgets.BNKT.input_frame.rowconfigure(0, weight=1)
    tk_widgets.BNKT.input_frame.rowconfigure(1, weight=1)
    tk_widgets.BNKT.input_frame.rowconfigure(2, weight=1)

    # create audio entry
    tk_widgets.BNKT.audio_entry = ctk.CTkEntry(
        tk_widgets.BNKT.input_frame,
        font=le_font
    )
    tk_widgets.BNKT.audio_entry.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create audio browse button

    def audiobrowse_cmd():
        audio_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select Audio BNK/WPK file',
            filetypes=(
                ('BNK/WPK files', ('*.bnk', '*.wpk')),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        if audio_path != '':
            tk_widgets.BNKT.audio_entry.delete(0, tk.END)
            tk_widgets.BNKT.audio_entry.insert(tk.END, audio_path)
    tk_widgets.BNKT.audiobrowse_button = ctk.CTkButton(
        tk_widgets.BNKT.input_frame,
        text='Browse Audio BNK/WPK',
        image=EmojiImage.create('🔈'),
        anchor=tk.CENTER,
        command=audiobrowse_cmd,
        font=le_font
    )
    tk_widgets.BNKT.audiobrowse_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create event entry
    tk_widgets.BNKT.event_entry = ctk.CTkEntry(
        tk_widgets.BNKT.input_frame,
        font=le_font
    )
    tk_widgets.BNKT.event_entry.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create event browse button

    def eventbrowse_cmd():
        event_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select Events BNK file',
            filetypes=(
                ('BNK files', '*.bnk'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        if event_path != '':
            tk_widgets.BNKT.event_entry.delete(0, tk.END)
            tk_widgets.BNKT.event_entry.insert(tk.END, event_path)
    tk_widgets.BNKT.audiobrowse_button = ctk.CTkButton(
        tk_widgets.BNKT.input_frame,
        text='Browse Events BNK',
        image=EmojiImage.create('📋'),
        anchor=tk.CENTER,
        command=eventbrowse_cmd,
        font=le_font
    )
    tk_widgets.BNKT.audiobrowse_button.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create bin entry
    tk_widgets.BNKT.bin_entry = ctk.CTkEntry(
        tk_widgets.BNKT.input_frame,
        font=le_font
    )
    tk_widgets.BNKT.bin_entry.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def binbrowse_cmd():
        bin_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        if bin_path != '':
            tk_widgets.BNKT.bin_entry.delete(0, tk.END)
            tk_widgets.BNKT.bin_entry.insert(tk.END, bin_path)
    # create bin browse button
    tk_widgets.BNKT.binbrowse_button = ctk.CTkButton(
        tk_widgets.BNKT.input_frame,
        text='Browse BIN',
        image=EmojiImage.create('📝'),
        anchor=tk.CENTER,
        command=binbrowse_cmd,
        font=le_font
    )
    tk_widgets.BNKT.binbrowse_button.grid(
        row=2, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create view frame
    tk_widgets.BNKT.view_frame = ctk.CTkFrame(
        tk_widgets.BNKT.page_frame
    )
    tk_widgets.BNKT.view_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.BNKT.view_frame.rowconfigure(0, weight=1)
    tk_widgets.BNKT.view_frame.columnconfigure(0, weight=9)
    tk_widgets.BNKT.view_frame.columnconfigure(1, weight=1)

    # create tree frame
    tk_widgets.BNKT.tree_frame = ctk.CTkFrame(
        tk_widgets.BNKT.view_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.BNKT.tree_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.BNKT.tree_frame.columnconfigure(0, weight=1)
    tk_widgets.BNKT.tree_frame.columnconfigure(1, weight=0)
    tk_widgets.BNKT.tree_frame.rowconfigure(0, weight=1)

    # create control frame
    tk_widgets.BNKT.control_frame = ctk.CTkFrame(
        tk_widgets.BNKT.view_frame
    )
    tk_widgets.BNKT.control_frame.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.BNKT.control_frame.columnconfigure(0, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(0, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(1, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(2, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(3, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(4, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(5, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(6, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(7, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(8, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(9, weight=1)
    tk_widgets.BNKT.control_frame.rowconfigure(10, weight=699)

    # create load button
    def load_cmd():
        if tk_widgets.BNKT.treeview != None:
            raise Exception('bnk_tool: Failed: There is already a treeview loaded, please click clear button to reset the app.')
        
        # read stuffs
        bnk_tool.BNKParser.reset_cache()
        parser = bnk_tool.BNKParser(
            audio_path=tk_widgets.BNKT.audio_entry.get(),
            events_path=tk_widgets.BNKT.event_entry.get(),
            bin_path=tk_widgets.BNKT.bin_entry.get()
        )
        parser.unpack(parser.get_cache_dir())
        
        # create treeview
        tk_widgets.BNKT.treeview = treeview = ttk.Treeview(
            tk_widgets.BNKT.tree_frame, 
            show='tree'
        )
        treeview.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        treeview.parser = parser

        # create scrollbar
        treeview.treeview_scrollbar = treeview_scrollbar = ctk.CTkScrollbar(
            tk_widgets.BNKT.tree_frame,
            command=treeview.yview
        )
        treeview_scrollbar.grid(row=0, column=1, padx=0, pady=0, sticky=tk.NSEW)
        treeview.configure(yscrollcommand=treeview_scrollbar.set)
        
        # pass data to the tree
        root_tree_id = ''
        treeview.cached_imgs = []
        for event_id  in parser.audio_tree:
            event_image = EmojiImage.create('📢', return_ctk=False)
            event_tree_id = treeview.insert(
                root_tree_id, 
                tk.END, 
                text=str(event_id), 
                image=event_image,
                tags='event'
            )
            treeview.cached_imgs.append(event_image)
            for container_id in parser.audio_tree[event_id]:
                container_image = EmojiImage.create('📣', return_ctk=False)
                container_tree_id = treeview.insert(
                    event_tree_id, 
                    tk.END, 
                    text=str(container_id), 
                    image=container_image,
                    tags='container'
                )
                treeview.cached_imgs.append(container_image)
                for wem_id in parser.audio_tree[event_id][container_id]:
                    wem_image = EmojiImage.create('🎵', return_ctk=False)
                    wem_tree_id = treeview.insert(
                        container_tree_id, 
                        tk.END, 
                        text=str(wem_id), 
                        image=wem_image,
                        tags='wem'
                    )
                    treeview.cached_imgs.append(wem_image)
        # treeview event 
        def wem_selected(event):
            tree = event.widget
            # this part is for replace button
            selected = [tree.item(item) for item in tree.selection()]
            wem_selected = [item for item in selected if item['tags'] == 'wem']
            # play focus item if its a wem
            if setting.get('bnktool.auto_play', 1) == 1:
                focus_item = tree.item(tree.focus())
                if focus_item['tags'][0] == 'wem':
                    wem_id = int(focus_item['text'])
                    parser.play(wem_id)

        treeview.bind('<<TreeviewSelect>>', wem_selected)

    tk_widgets.BNKT.load_button = ctk.CTkButton(
        tk_widgets.BNKT.control_frame,
        text='Load',
        image=EmojiImage.create('💿'),
        anchor=tk.CENTER,
        command=load_cmd,
        font=le_font
    )
    tk_widgets.BNKT.load_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    # create save button
    def save_cmd():
        def save_thrd():
            if tk_widgets.BNKT.treeview != None:
                parser = tk_widgets.BNKT.treeview.parser 
                if parser.bnk_audio_parsing:
                    output_file = tkfd.asksaveasfilename(
                        parent=tk_widgets.main_tk,
                        title='Chhose Audio BNK path to save',
                        filetypes=(
                            ('BNK files', '*.bnk'),
                            ('All files', '*.*'),
                        ),
                        defaultextension='.bnk',
                        initialdir=setting.get('default_folder', None)
                    )
                else:
                    output_file = tkfd.asksaveasfilename(
                        parent=tk_widgets.main_tk,
                        title='Chhose Audio WPK path to save',
                        filetypes=(
                            ('WPK files', '*.wpk'),
                            ('All files', '*.*'),
                        ),
                        defaultextension='.wpk',
                        initialdir=setting.get('default_folder', None)
                    )
                if output_file != '':
                    parser.pack(output_file)
                    LOG(f'bnk_tool: Done: Save Audio BNK/WPK: {output_file}')
    
        if check_thread_safe(tk_widgets.BNKT.working_thread):
            tk_widgets.BNKT.working_thread = Thread(target=save_thrd, daemon=True)
            tk_widgets.BNKT.working_thread.start()
        else:
            LOG(
                'bnk_tool: Failed: A thread is already running, wait for it to finished.')
            
    tk_widgets.BNKT.save_button = ctk.CTkButton(
        tk_widgets.BNKT.control_frame,
        text='Save',
        image=EmojiImage.create('💾'),
        anchor=tk.CENTER,
        command=save_cmd,
        font=le_font
    )
    tk_widgets.BNKT.save_button.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
    # create clear button
    def clear_cmd():
        if tk_widgets.BNKT.treeview != None:
            tk_widgets.BNKT.treeview.treeview_scrollbar.destroy()
            tk_widgets.BNKT.treeview.destroy()
            tk_widgets.BNKT.treeview = None
        bnk_tool.BNKParser.reset_cache()

    tk_widgets.BNKT.clear_button = ctk.CTkButton(
        tk_widgets.BNKT.control_frame,
        text='Clear',
        image=EmojiImage.create('❌'),
        anchor=tk.CENTER,
        command=clear_cmd,
        font=le_font
    )
    tk_widgets.BNKT.clear_button.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    # create extract button
    def extract_cmd():
        def extract_thrd():
            if tk_widgets.BNKT.treeview != None:
                output_dir = tkfd.askdirectory(
                    parent=tk_widgets.main_tk,
                    title='Select Default Folder',
                    initialdir=setting.get('default_folder', None)
                )
                if output_dir != '':
                    tree = tk_widgets.BNKT.treeview
                    tree.parser.extract(output_dir, convert_ogg=False)
                    LOG(f'bnk_tool: Done: Extract all wems: {output_dir}')
        
        if check_thread_safe(tk_widgets.BNKT.working_thread):
            tk_widgets.BNKT.working_thread = Thread(target=extract_thrd, daemon=True)
            tk_widgets.BNKT.working_thread.start()
        else:
            LOG(
                'bnk_tool: Failed: A thread is already running, wait for it to finished.')
            
    tk_widgets.BNKT.extract_button = ctk.CTkButton(
        tk_widgets.BNKT.control_frame,
        text='Extract all wems',
        image=EmojiImage.create('➡️', weird=True),
        anchor=tk.CENTER,
        command=extract_cmd,
        font=le_font
    )
    tk_widgets.BNKT.extract_button.grid(
        row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    # create replace button
    def replace_cmd():
        LOG('not yet supported this version')
    tk_widgets.BNKT.replace_button = ctk.CTkButton(
        tk_widgets.BNKT.control_frame,
        text='Replace wem data',
        image=EmojiImage.create('🔁'),
        anchor=tk.CENTER,
        command=replace_cmd,
        font=le_font
    )
    tk_widgets.BNKT.replace_button.grid(
        row=4, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    # create play button
    def play_cmd():
        if tk_widgets.BNKT.treeview != None:
            tree = tk_widgets.BNKT.treeview
            if tree != None:
                # this part is for replace button
                selected = [tree.item(item) for item in tree.selection()]
                wem_selected = [item for item in selected if item['tags'] == 'wem']
                # play focus item if its a wem
                focus_item = tree.item(tree.focus())
                if focus_item['tags'][0] == 'wem':
                    wem_id = int(focus_item['text'])
                    tree.parser.play(wem_id)
    tk_widgets.BNKT.play_button = ctk.CTkButton(
        tk_widgets.BNKT.control_frame,
        text='Play selected',
        image=EmojiImage.create('▶️', weird=True),
        anchor=tk.CENTER,
        command=play_cmd,
        font=le_font
    )
    tk_widgets.BNKT.play_button.grid(
        row=5, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    # create stop button
    def stop_cmd():
        if tk_widgets.BNKT.treeview != None:
            tree = tk_widgets.BNKT.treeview
            if tree != None:
                tree.parser.stop()
    tk_widgets.BNKT.stop_button = ctk.CTkButton(
        tk_widgets.BNKT.control_frame,
        text='Stop all playing sounds',
        image=EmojiImage.create('⏹️', weird=True),
        anchor=tk.CENTER,
        command=stop_cmd,
        font=le_font
    )
    tk_widgets.BNKT.stop_button.grid(
        row=6, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    # create auto play check box
    def autoplay_cmd():
        setting.set('bnktool.auto_play',
                    tk_widgets.BNKT.autoplay_checkbox.get())
        setting.save()
    tk_widgets.BNKT.autoplay_checkbox = ctk.CTkCheckBox(
        tk_widgets.BNKT.control_frame,
        text='Auto Play',
        command=autoplay_cmd,
        font=le_font
    )
    tk_widgets.BNKT.autoplay_checkbox.grid(
        row=7, column=0, padx=5, pady=5, sticky=tk.NSEW)
    if setting.get('bnktool.auto_play', 1) == 1:
        tk_widgets.BNKT.autoplay_checkbox.select()
    else:
        tk_widgets.BNKT.autoplay_checkbox.deselect()

    # create volume label
    tk_widgets.BNKT.volume_label = ctk.CTkLabel(
        tk_widgets.BNKT.control_frame,
        text = 'Volume:',
        anchor = tk.W,
        font=le_font
    )
    tk_widgets.BNKT.volume_label.grid(
        row=8, column=0, padx=5, pady=5, sticky=tk.NSEW)
    
    # create volume slider
    tk_widgets.BNKT.volume_slider = ctk.CTkSlider(
        tk_widgets.BNKT.control_frame
    )
    tk_widgets.BNKT.volume_slider.grid(
        row=9, column=0, padx=5, pady=5, sticky=tk.NSEW)


def create_DDSM_page():    
    tk_widgets.DDSM.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.DDSM.page_frame.columnconfigure(0, weight=1)
    tk_widgets.DDSM.page_frame.rowconfigure(0, weight=1)
    # init stuffs
    tk_widgets.DDSM.working_thread = None
    # create action frame
    tk_widgets.DDSM.action_frame = ctk.CTkFrame(
        tk_widgets.DDSM.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.DDSM.action_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.DDSM.action_frame.columnconfigure(0, weight=1)
    tk_widgets.DDSM.action_frame.columnconfigure(1, weight=1)
    tk_widgets.DDSM.action_frame.columnconfigure(2, weight=699)
    tk_widgets.DDSM.action_frame.rowconfigure(0, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(1, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(2, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(3, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(4, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(5, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(6, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(7, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(8, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(9, weight=1)
    tk_widgets.DDSM.action_frame.rowconfigure(10, weight=699)
    
    # create dds2png label
    tk_widgets.DDSM.dds2png_label = ctk.CTkLabel(
        tk_widgets.DDSM.action_frame,
        text = 'DDS to PNG',
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.DDSM.dds2png_label.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create dds2png button
    def dds2png_cmd(isdir=False):
        def dds2png_thrd():
            if isdir:
                dir_path = tkfd.askdirectory(
                    parent=tk_widgets.main_tk,
                    title='Select Default Folder',
                    initialdir=setting.get('default_folder', None)
                )
                dds_paths = []
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.dds'):
                            dds_paths.append(os.path.join(root, file).replace('\\', '/'))
            else:
                dds_paths = tkfd.askopenfilenames(
                    title='Select DDS',
                    parent=tk_widgets.main_tk,
                    filetypes=(('DDS file', '*.dds'),),
                    initialdir=setting.get('default_folder', None)
                )
            if len(dds_paths) > 0:
                LOG(f'ddsmart: Running: dds2png: {len(dds_paths)} items.')
                for dds_path in dds_paths:
                    ext_tools.ImageMagick.to_png(
                        src=dds_path,
                        png=dds_path.replace('.dds', '.png')
                    )
                LOG(f'ddsmart: Done: dds2png: {len(dds_paths)} items.')
        
        if check_thread_safe(tk_widgets.DDSM.working_thread):
            tk_widgets.DDSM.working_thread = Thread(target=dds2png_thrd, daemon=True)
            tk_widgets.DDSM.working_thread.start()
        else:
            LOG(
                'ddsmart: Failed: A thread is already running, wait for it to finished.')
        
    tk_widgets.DDSM.dds2png_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select DDS',
        image=EmojiImage.create('🏞️', weird=True),
        anchor=tk.CENTER,
        command=lambda: dds2png_cmd(isdir=False),
        font=le_font
    )
    tk_widgets.DDSM.dds2png_button.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.DDSM.dds2png_dir_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=lambda: dds2png_cmd(isdir=True),
        font=le_font
    )
    tk_widgets.DDSM.dds2png_dir_button.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
    
    # create png2dds label
    tk_widgets.DDSM.png2dds_label = ctk.CTkLabel(
        tk_widgets.DDSM.action_frame,
        text='PNG to DDS',
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.DDSM.png2dds_label.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create png2dds button
    def png2dds_cmd(isdir=False):
        def png2dds_thrd():
            if isdir:
                dir_path = tkfd.askdirectory(
                    parent=tk_widgets.main_tk,
                    title='Select Default Folder',
                    initialdir=setting.get('default_folder', None)
                )
                png_paths = []
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.png'):
                            png_paths.append(os.path.join(root, file).replace('\\', '/'))
            else:
                png_paths = tkfd.askopenfilenames(
                    title='Select PNG',
                    parent=tk_widgets.main_tk,
                    filetypes=(('PNG file', '*.png'),),
                    initialdir=setting.get('default_folder', None)
                )
            if len(png_paths) > 0:
                LOG(f'ddsmart: Running: png2dds: {len(png_paths)} items.')
                for png_path in png_paths:
                    ext_tools.ImageMagick.to_dds(
                        src=png_path,
                        dds=png_path.replace('.png', '.dds')
                    )
                LOG(f'ddsmart: Done: png2dds: {len(png_paths)} items.')
        
        if check_thread_safe(tk_widgets.DDSM.working_thread):
            tk_widgets.DDSM.working_thread = Thread(target=png2dds_thrd, daemon=True)
            tk_widgets.DDSM.working_thread.start()
        else:
            LOG(
                'ddsmart: Failed: A thread is already running, wait for it to finished.')
    tk_widgets.DDSM.png2dds_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select PNG',
        image=EmojiImage.create('🌇'),
        anchor=tk.CENTER,
        command=lambda: png2dds_cmd(isdir=False),
        font=le_font
    )
    tk_widgets.DDSM.png2dds_button.grid(
        row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.DDSM.png2dds_dir_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=lambda: png2dds_cmd(isdir=True),
        font=le_font
    )
    tk_widgets.DDSM.png2dds_dir_button.grid(
        row=3, column=1, padx=5, pady=5, sticky=tk.NSEW)
    

    # create dds2tex label
    tk_widgets.DDSM.dds2tex_label = ctk.CTkLabel(
        tk_widgets.DDSM.action_frame,
        text = 'DDS to TEX',
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.DDSM.dds2tex_label.grid(
        row=4, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create dds2tex button
    def dds2tex_cmd(isdir=False):
        def dds2tex_thrd():
            if isdir:
                dir_path = tkfd.askdirectory(
                    parent=tk_widgets.main_tk,
                    title='Select Default Folder',
                    initialdir=setting.get('default_folder', None)
                )
                dds_paths = []
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.dds'):
                            dds_paths.append(os.path.join(root, file).replace('\\', '/'))
            else:
                dds_paths = tkfd.askopenfilenames(
                    title='Select DDS',
                    parent=tk_widgets.main_tk,
                    filetypes=(('DDS file', '*.dds'),),
                    initialdir=setting.get('default_folder', None)
                )
            if len(dds_paths) > 0:
                LOG(f'ddsmart: Running: dds2tex: {len(dds_paths)} items.')
                for dds_path in dds_paths:
                    Ritoddstex.dds2tex(dds_path)
                LOG(f'ddsmart: Done: dds2tex: {len(dds_paths)} items.')
        
        if check_thread_safe(tk_widgets.DDSM.working_thread):
            tk_widgets.DDSM.working_thread = Thread(target=dds2tex_thrd, daemon=True)
            tk_widgets.DDSM.working_thread.start()
        else:
            LOG(
                'ddsmart: Failed: A thread is already running, wait for it to finished.')
    tk_widgets.DDSM.dds2tex_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select DDS',
        image=EmojiImage.create('🏞️', weird=True),
        anchor=tk.CENTER,
        command=lambda: dds2tex_cmd(isdir=False),
        font=le_font
    )
    tk_widgets.DDSM.dds2tex_button.grid(
        row=5, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.DDSM.dds2tex_dir_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=lambda: dds2tex_cmd(isdir=True),
        font=le_font
    )
    tk_widgets.DDSM.dds2tex_dir_button.grid(
        row=5, column=1, padx=5, pady=5, sticky=tk.NSEW)


    # create tex2dds label
    tk_widgets.DDSM.tex2dds_label = ctk.CTkLabel(
        tk_widgets.DDSM.action_frame,
        text = 'TEX to DDS',
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.DDSM.tex2dds_label.grid(
        row=6, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create tex2dds button
    def tex2dds_cmd(isdir=False):
        def tex2dds_thrd():
            if isdir:
                dir_path = tkfd.askdirectory(
                    parent=tk_widgets.main_tk,
                    title='Select Default Folder',
                    initialdir=setting.get('default_folder', None)
                )
                tex_paths = []
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.tex'):
                            tex_paths.append(os.path.join(root, file).replace('\\', '/'))
            else:
                tex_paths = tkfd.askopenfilenames(
                    title='Select TEX',
                    parent=tk_widgets.main_tk,
                    filetypes=(('TEX file', '*.tex'),),
                    initialdir=setting.get('default_folder', None)
                )
            if len(tex_paths) > 0:
                LOG(f'ddsmart: Running: tex2dds: {len(tex_paths)} items.')
                for tex_path in tex_paths:
                    Ritoddstex.tex2dds(tex_path)
                LOG(f'ddsmart: Done: tex2dds: {len(tex_paths)} items.')
        
        if check_thread_safe(tk_widgets.DDSM.working_thread):
            tk_widgets.DDSM.working_thread = Thread(target=tex2dds_thrd, daemon=True)
            tk_widgets.DDSM.working_thread.start()
        else:
            LOG(
                'ddsmart: Failed: A thread is already running, wait for it to finished.')
    tk_widgets.DDSM.tex2dds_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select TEX',
        image=EmojiImage.create('🌌'),
        anchor=tk.CENTER,
        command=lambda: tex2dds_cmd(isdir=False),
        font=le_font
    )
    tk_widgets.DDSM.tex2dds_button.grid(
        row=7, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.DDSM.tex2dds_dir_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=lambda: tex2dds_cmd(isdir=True),
        font=le_font
    )
    tk_widgets.DDSM.tex2dds_dir_button.grid(
        row=7, column=1, padx=5, pady=5, sticky=tk.NSEW)

    
    # create make2x4xdds label
    tk_widgets.DDSM.make2x4xdds_label = ctk.CTkLabel(
        tk_widgets.DDSM.action_frame,
        text = 'Make 2x, 4x DDS',
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.DDSM.make2x4xdds_label.grid(
        row=8, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create make2x4xdds button
    def make2x4xdds_cmd(isdir=False):
        def make2x4xdds_thrd():
            if isdir:
                dir_path = tkfd.askdirectory(
                    parent=tk_widgets.main_tk,
                    title='Select Default Folder',
                    initialdir=setting.get('default_folder', None)
                )
                dds_paths = []

                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.dds') and file[:3] not in ('2x_', '4x_'):
                                dds_paths.append(os.path.join(root, file).replace('\\', '/'))
            else:
                dds_paths = tkfd.askopenfilenames(
                    title='Select DDS',
                    parent=tk_widgets.main_tk,
                    filetypes=(('DDS file', '*.dds'),),
                    initialdir=setting.get('default_folder', None)
                )
            if len(dds_paths) > 0:
                LOG(f'ddsmart: Running: make2x4xdds: {len(dds_paths)} items.')
                for dds_path in dds_paths:
                    src = dds_path
                    with Image.open(src) as img:
                        basename = os.path.basename(src)
                        dirname = os.path.dirname(src)
                        width_2x = img.width // 2
                        height_2x = img.height // 2
                        file_2x = os.path.join(dirname, '2x_'+basename).replace('\\', '/')
                        width_4x = img.width // 4
                        height_4x = img.height // 4
                        file_4x = os.path.join(dirname, '4x_'+basename).replace('\\', '/')
                    if not os.path.exists(file_2x):
                        ext_tools.ImageMagick.resize_dds(
                            src=src,
                            dst=file_2x, width=width_2x, height=height_2x
                        )
                    if not os.path.exists(file_4x):
                        ext_tools.ImageMagick.resize_dds(
                            src=src,
                            dst=file_4x, width=width_4x, height=height_4x
                        )
                LOG(f'ddsmart: Done: make2x4xdds: {len(dds_paths)} items.')
        
        if check_thread_safe(tk_widgets.DDSM.working_thread):
            tk_widgets.DDSM.working_thread = Thread(target=make2x4xdds_thrd, daemon=True)
            tk_widgets.DDSM.working_thread.start()
        else:
            LOG(
                'ddsmart: Failed: A thread is already running, wait for it to finished.')
    tk_widgets.DDSM.make2x4xdds_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select DDS',
        image=EmojiImage.create('🏞️', weird=True),
        anchor=tk.CENTER,
        command=lambda: make2x4xdds_cmd(isdir=False),
        font=le_font
    )
    tk_widgets.DDSM.make2x4xdds_button.grid(
        row=9, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.DDSM.make2x4xdds_dir_button = ctk.CTkButton(
        tk_widgets.DDSM.action_frame,
        text='Select Folder',
        image=EmojiImage.create('📁'),
        anchor=tk.CENTER,
        command=lambda: make2x4xdds_cmd(isdir=True),
        font=le_font
    )
    tk_widgets.DDSM.make2x4xdds_dir_button.grid(
        row=9, column=1, padx=5, pady=5, sticky=tk.NSEW)



def create_ST_page():
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
    # general label
    tk_widgets.ST.general_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='General',
        font=le_font
    )
    tk_widgets.ST.general_label.grid(
        row=0, column=0, padx=10, pady=5, sticky=tk.NSEW)
    # appearance mode 
    tk_widgets.ST.appearance_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Appearance:',
        image=EmojiImage.create('☀️', weird=True),
        compound=tk.LEFT,
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.ST.appearance_label.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def appearance_cmd(choice):
        setting.set('appearance', choice)
        setting.save()
        LOG('setting: Restart is require for appearance/style/theme changes to take effect.')
    tk_widgets.ST.appearance_option = ctk.CTkOptionMenu(
        tk_widgets.ST.scroll_frame,
        values=[
            'light',
            'dark',
            'system'
        ],
        command=appearance_cmd,
        font=le_font
    )
    tk_widgets.ST.appearance_option.set(setting.get('appearance', 'system'))
    tk_widgets.ST.appearance_option.grid(
        row=1, column=2, padx=5, pady=5, sticky=tk.NSEW)
    
    # style
    tk_widgets.ST.style_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Style:',
        image=EmojiImage.create('✨'),
        compound=tk.LEFT,
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.ST.style_label.grid(
        row=2, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def style_cmd(choice):
        setting.set('style', choice)
        setting.save()
        LOG('setting: Restart is require for appearance/style/theme changes to take effect.')
    tk_widgets.ST.style_option = ctk.CTkOptionMenu(
        tk_widgets.ST.scroll_frame,
        values=[
            'system',
            'mica',
            'acrylic',
            'aero',
            'transparent',
            'optimised',
            'win7',
            'inverse'
        ],
        command=style_cmd,
        font=le_font
    )
    tk_widgets.ST.style_option.set(setting.get('style', 'system'))
    tk_widgets.ST.style_option.grid(
        row=2, column=2, padx=5, pady=5, sticky=tk.NSEW)

    # theme
    tk_widgets.ST.theme_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Theme:',
        image=EmojiImage.create('🖌️', weird=True),
        compound=tk.LEFT,
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.ST.theme_label.grid(
        row=3, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def theme_cmd(choice):
        set_theme(choice)
        setting.set('theme', choice)
        setting.save()
        LOG('setting: Restart is require for appearance/style/theme changes to take effect.')
    tk_widgets.ST.theme_option = ctk.CTkOptionMenu(
        tk_widgets.ST.scroll_frame,
        values=[
            'blue',
            'dark-blue',
            'green',
            'carrot',
            'coffee',
            'marsh',
            'metal',
            'pink',
            'red',
            'sky',
            'violet',
            'yellow',
        ],
        command=theme_cmd,
        font=le_font
    )
    tk_widgets.ST.theme_option.set(setting.get('theme', 'blue'))
    tk_widgets.ST.theme_option.grid(
        row=3, column=2, padx=5, pady=5, sticky=tk.NSEW)
    
    # limit message
    tk_widgets.ST.loglimit_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Log Limit Messages:',
        image=EmojiImage.create('🗒️', weird=True),
        compound=tk.LEFT,
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.ST.loglimit_label.grid(
        row=4, column=1, padx=5, pady=5, sticky=tk.NSEW)

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
        command=loglimit_cmd,
        font=le_font
    )
    tk_widgets.ST.loglimit_option.set(setting.get('Log.limit', '100'))
    tk_widgets.ST.loglimit_option.grid(
        row=4, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # shortcut desktop
    tk_widgets.ST.desktop_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Create Desktop Shortcut',
        image=EmojiImage.create('🖥️', weird=True),
        anchor=tk.W,
        command=winLT.Shortcut.create_desktop,
        font=le_font
    )
    tk_widgets.ST.desktop_button.grid(
        row=5, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # explorer context
    tk_widgets.ST.contextadd_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Create Explorer Contexts',
        image=EmojiImage.create('💬'),
        anchor=tk.W,
        command=winLT.Context.create_contexts,
        font=le_font
    )
    tk_widgets.ST.contextadd_button.grid(
        row=6, column=1, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.ST.contextrmv_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Remove Explorer Contexts',
        image=EmojiImage.create('❌'),
        anchor=tk.W,
        command=winLT.Context.remove_contexts,
        font=le_font
    )
    tk_widgets.ST.contextrmv_button.grid(
        row=6, column=2, padx=5, pady=5, sticky=tk.NS+tk.W)
    # default folder
    tk_widgets.ST.defaultdir_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Ask Default Folder:',
        image=EmojiImage.create('🌳'),
        compound=tk.LEFT,
        anchor=tk.W,
        font=le_font
    )
    tk_widgets.ST.defaultdir_label.grid(
        row=7, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def defaultdir_cmd():
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select Default Folder',
            initialdir=setting.get('default_folder', None)
        )
        if dir_path == '':
            dir_path = None
            tk_widgets.ST.defaultdir_value_label.configure(
                text='Default folder for all ask-file/ask-folder dialogs.'
            )
        else:
            tk_widgets.ST.defaultdir_value_label.configure(text=dir_path)
        setting.set('default_folder', dir_path)
        setting.save()

    tk_widgets.ST.defaultdir_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Browse',
        image=EmojiImage.create('📁'),
        command=defaultdir_cmd,
        font=le_font
    )
    tk_widgets.ST.defaultdir_button.grid(
        row=7, column=2, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.ST.defaultdir_value_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        anchor=tk.W,
        font=le_font
    )
    defaultdir = setting.get('default_dir', None)
    if defaultdir == None:
        tk_widgets.ST.defaultdir_value_label.configure(
            text='Default folder for all ask-file/ask-folder dialog'
        )
    tk_widgets.ST.defaultdir_value_label.grid(
        row=7, column=3, padx=5, pady=5, sticky=tk.NSEW)
    # restart ltmao
    def restart_cmd():
        import sys
        LOG(f'Running: Restart LtMAO')
        os.system(os.path.join(os.path.abspath(os.path.curdir),'start.bat'))
        tk_widgets.main_tk.destroy()
        sys.exit(0)
        
    tk_widgets.ST.restart_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Restart LtMAO',
        image=EmojiImage.create('🚀'),
        anchor=tk.W,
        command=restart_cmd,
        font=le_font
    )
    tk_widgets.ST.restart_button.grid(
        row=8, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # update ltmao
    def update_cmd():
        def update_thrd():
            def to_human(size): 
                return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + ["", " KB", " MB", " GB", " TB", " PB", " EB"][max(size.bit_length()-1, 0)//10]
            
            check_version()
            
            if VERSION == NEW_VERSION:
                LOG('update: Failed: Current version {VERSION} is the latest version.')
            else:
                local_file = './LtMAO-master.zip'
                remote_file = 'https://codeload.github.com/tarngaina/LtMAO/zip/refs/heads/master'
                # GET request
                get = requests.get(remote_file, stream=True)
                get.raise_for_status()
                # download update
                bytes_downloaded = 0
                chunk_size = 1024**2*5
                bytes_downloaded_log = 0
                bytes_downloaded_log_limit = 1024**2
                with open(local_file, 'wb') as f:
                    for chunk in get.iter_content(chunk_size):
                        chunk_length = len(chunk)
                        bytes_downloaded += chunk_length
                        f.write(chunk)
                        bytes_downloaded_log += chunk_length
                        if bytes_downloaded_log > bytes_downloaded_log_limit:
                            LOG(
                                f'update: Downloading: {remote_file}: {to_human(bytes_downloaded)}')
                            bytes_downloaded_log = 0
                LOG(f'update: Done: Downloaded: {local_file}')
                # extract update
                from zipfile import ZipFile
                with ZipFile(local_file) as zip:
                    for zipinfo in zip.infolist():
                        zipinfo.filename = zipinfo.filename.replace('LtMAO-master/', '')
                        try:
                            zip.extract(zipinfo, '.')
                        except Exception as e:
                            LOG(f'update: Failed but Ignored: Extract: {zipinfo.filename}: {e}')
                # remove update file
                os.remove(local_file)
                # restat ltmao
                import sys
                LOG(f'Running: Restart LtMAO')
                os.system(os.path.join(os.path.abspath(os.path.curdir),'start.bat'))
                tk_widgets.main_tk.destroy()
                sys.exit(0)

        Thread(target=update_thrd, daemon=True).start()

    tk_widgets.ST.update_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Update LtMAO',
        image=EmojiImage.create('🚨'),
        anchor=tk.W,
        command=update_cmd,
        font=le_font
    )
    tk_widgets.ST.update_button.grid(
        row=9, column=1, padx=5, pady=5, sticky=tk.NSEW)


def create_CL_page():
    tk_widgets.CL.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.CL.page_frame.columnconfigure(0, weight=1)
    tk_widgets.CL.page_frame.rowconfigure(0, weight=1)
        
    # create changelog textbox
    tk_widgets.CL.changelog_text = ctk.CTkTextbox(
        tk_widgets.CL.page_frame,
        state=tk.DISABLED,
        wrap=tk.WORD,
        font=le_font
    )
    tk_widgets.CL.changelog_text.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.CL.changelog_text.configure(state=tk.NORMAL)
    tk_widgets.CL.changelog_text.insert(tk.END, 'Loading...')
    tk_widgets.CL.changelog_text.configure(state=tk.DISABLED)
    
    # get changelog too because 1 time get anyway
    def get_changelog_cmd():
        full_changelog_text = ''
        local_file = './prefs/changelog.txt'
        try:
            page = 1
            while True:
                url=f'https://api.github.com/repos/tarngaina/ltmao/commits?per_page=100&page={page}'
                commits=requests.get(url).json()
                if len(commits) > 0:
                    for commit in commits:
                        commit = commit['commit']
                        
                        author = commit['author']['name']
                        date = commit['author']['date']
                        message = commit['message']
                        full_changelog_text += f'[{date}] by {author}:\n{message}\n\n'
                else:
                    break
                page+=1
            with open(local_file, 'w+') as f:
                f.write(full_changelog_text)
        except Exception as e:
            LOG(f'get_changelog: Failed: {e}, switching to local file if exists.')
            if os.path.exists(local_file):
                with open(local_file, 'r') as f:
                    full_changelog_text = f.read()
            else:
                full_changelog_text = 'Failed to download changelog and no local changelog to read.'
        tk_widgets.CL.changelog_text.configure(state=tk.NORMAL)
        tk_widgets.CL.changelog_text.delete('1.0', tk.END)
        tk_widgets.CL.changelog_text.insert(tk.END, full_changelog_text)
        tk_widgets.CL.changelog_text.configure(state=tk.DISABLED)

    Thread(target=get_changelog_cmd, daemon=True).start()
        

def select_right_page(selected):
    # hide all page
    for page in tk_widgets.pages:
        if page.page_frame != None:
            page.page_frame.grid_forget()
    tk_widgets.LOG.page_frame.grid_forget()
    tk_widgets.ST.page_frame.grid_forget()
    tk_widgets.CL.page_frame.grid_forget()
    # show selected page
    if selected < 999:
        # tool pages
        if tk_widgets.pages[selected].page_frame == None:
            # create selected tool page
            create_func = tk_widgets.create_right_page[selected]
            if create_func != None:
                create_func()
        # show selected tool page
        page_frame = tk_widgets.pages[selected].page_frame
        if page_frame != None:
            page_frame.grid(
                row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 999:
        # log page
        tk_widgets.LOG.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    elif selected == 1000:
        # setting page
        tk_widgets.ST.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)
    else:
        # changelog page
        tk_widgets.CL.page_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)


def create_page_controls():
    tk_widgets.mainright_frame.columnconfigure(0, weight=1)
    tk_widgets.mainright_frame.rowconfigure(0, weight=1)
    tk_widgets.mainleft_frame.columnconfigure(0, weight=1)

    def control_cmd(page):
        # non active all controls
        for control_button in tk_widgets.control_buttons:
            control_button.configure(
                fg_color=tk_widgets.c_nonactive_fg,
                text_color=tk_widgets.c_nonactive_text
            )
        if tk_widgets.minilog_control != None:
            tk_widgets.minilog_control.configure(
                fg_color=tk_widgets.c_nonactive_fg,
                text_color=tk_widgets.c_nonactive_text
            )
        if tk_widgets.setting_control != None:
            tk_widgets.setting_control.configure(
                fg_color=tk_widgets.c_nonactive_fg,
                text_color=tk_widgets.c_nonactive_text
            )
        if tk_widgets.changelog_control != None:
            tk_widgets.changelog_control.configure(
                fg_color=tk_widgets.c_nonactive_fg,
                text_color=tk_widgets.c_nonactive_text
            )
        # active selected control
        if page < 999:
            # active selected tool control
            tk_widgets.control_buttons[page].configure(
                fg_color=tk_widgets.c_active_fg,
                text_color=tk_widgets.c_active_text
            )
        elif page == 999:
            # log control
            tk_widgets.minilog_control.configure(
                fg_color=tk_widgets.c_active_fg,
                text_color=tk_widgets.c_active_text
            )
        elif page == 1000:
            # setting control
            tk_widgets.setting_control.configure(
                fg_color=tk_widgets.c_active_fg,
                text_color=tk_widgets.c_active_text
            )
        else:
            # changelog control
            tk_widgets.changelog_control.configure(
                fg_color=tk_widgets.c_active_fg,
                text_color=tk_widgets.c_active_text
            )

        # show page
        select_right_page(page)
    # create left controls buttons
    tk_widgets.select_control = control_cmd
    tk_widgets.control_buttons = [
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='cslmao',
            image=EmojiImage.create('🕹️', weird=True),
            command=lambda: control_cmd(0),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='leaguefile_inspector',
            image=EmojiImage.create('🔎'),
            command=lambda: control_cmd(1),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='animask_viewer',
            image=EmojiImage.create('🎬'),
            command=lambda: control_cmd(2),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='hash_manager',
            image=EmojiImage.create('📖'),
            command=lambda: control_cmd(3),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='vo_helper',
            image=EmojiImage.create('🗣️', weird=True),
            command=lambda: control_cmd(4),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='no_skin',
            image=EmojiImage.create('🚫'),
            command=lambda: control_cmd(5),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='uvee',
            image=EmojiImage.create('🧱'),
            command=lambda: control_cmd(6),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='shrum',
            image=EmojiImage.create('✏️', weird=True),
            command=lambda: control_cmd(7),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='hapiBin',
            image=EmojiImage.create('🐱'),
            command=lambda: control_cmd(8),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='wad_tool',
            image=EmojiImage.create('📦'),
            command=lambda: control_cmd(9),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='pyntex',
            image=EmojiImage.create('🕵🏻', weird=True),
            command=lambda: control_cmd(10),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='sborf',
            image=EmojiImage.create('🛠️', weird=True),
            command=lambda: control_cmd(11),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='lol2fbx',
            image=EmojiImage.create('💎'),
            command=lambda: control_cmd(12),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='bnk_tool',
            image=EmojiImage.create('🔊'),
            command=lambda: control_cmd(13),
            font=le_font
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='ddsmart',
            image=EmojiImage.create('🛣️', weird=True),
            command=lambda: control_cmd(14),
            font=le_font
        )
    ]
    for id, control_button in enumerate(tk_widgets.control_buttons):
        control_button.grid(
            row=id, column=0, padx=5, pady=5, sticky=tk.N+tk.EW)
        tk_widgets.mainleft_frame.rowconfigure(id, weight=1)
    tk_widgets.mainleft_frame.rowconfigure(
        len(tk_widgets.control_buttons), weight=699)
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
    tk_widgets.CSLMAO = tk_widgets.pages[0]
    tk_widgets.LFI = tk_widgets.pages[1]
    tk_widgets.AMV = tk_widgets.pages[2]
    tk_widgets.HM = tk_widgets.pages[3]
    tk_widgets.VH = tk_widgets.pages[4]
    tk_widgets.NS = tk_widgets.pages[5]
    tk_widgets.UVEE = tk_widgets.pages[6]
    tk_widgets.SHR = tk_widgets.pages[7]
    tk_widgets.HP = tk_widgets.pages[8]
    tk_widgets.WT = tk_widgets.pages[9]
    tk_widgets.PT = tk_widgets.pages[10]
    tk_widgets.SBORF = tk_widgets.pages[11]
    tk_widgets.LOLFBX = tk_widgets.pages[12]
    tk_widgets.BNKT = tk_widgets.pages[13]
    tk_widgets.DDSM = tk_widgets.pages[14]
    # create right pages
    tk_widgets.create_right_page = [
        create_CSLMAO_page,
        create_LFI_page,
        create_AMV_page,
        create_HM_page,
        create_VH_page,
        create_NS_page,
        create_UVEE_page,
        create_SHR_page,
        create_HP_page,
        create_WT_page,
        create_PT_page,
        create_SBORF_page,
        create_LOLFBX_page,
        create_BNKT_page,
        create_DDSM_page
    ]
    # create LOG and ST control, page
    tk_widgets.minilog_control = None
    tk_widgets.setting_control = None
    tk_widgets.LOG = Keeper()
    tk_widgets.ST = Keeper()
    tk_widgets.CL = Keeper()
    create_LOG_page()
    create_ST_page()
    create_CL_page()

def create_bottom_widgets():
    tk_widgets.mainbottom_frame.columnconfigure(0, weight=999)
    tk_widgets.mainbottom_frame.columnconfigure(1, weight=1)
    tk_widgets.mainbottom_frame.columnconfigure(2, weight=1)
    tk_widgets.mainbottom_frame.rowconfigure(0, weight=1)
    tk_widgets.bottom_widgets = Keeper()
    # create mini log
    tk_widgets.bottom_widgets.minilog_button = ctk.CTkButton(
        tk_widgets.mainbottom_frame,
        text='',
        anchor=tk.W,
        image=EmojiImage.create('🗒️', weird=True),
        command=lambda: tk_widgets.select_control(999)
    )
    tk_widgets.bottom_widgets.minilog_button.grid(
        row=0, column=0, padx=(10, 5), pady=0, sticky=tk.NSEW)
    Log.tk_minilog = tk_widgets.bottom_widgets.minilog_button
    tk_widgets.minilog_control = tk_widgets.bottom_widgets.minilog_button

    # create setting button
    tk_widgets.bottom_widgets.setting_button = ctk.CTkButton(
        tk_widgets.mainbottom_frame,
        text='Setting',
        anchor=tk.CENTER,
        image=EmojiImage.create('⚙️', weird=True),
        command=lambda: tk_widgets.select_control(1000),
        font=le_font
    )
    tk_widgets.bottom_widgets.setting_button.grid(
        row=0, column=1, padx=0, pady=0, sticky=tk.NSEW)
    tk_widgets.setting_control = tk_widgets.bottom_widgets.setting_button

    # create changelog button
    tk_widgets.bottom_widgets.changelog_button = ctk.CTkButton(
        tk_widgets.mainbottom_frame,
        text='Changelog',
        anchor=tk.CENTER,
        image=EmojiImage.create('📑'),
        command=lambda: tk_widgets.select_control(1001),
        font=le_font
    )
    tk_widgets.bottom_widgets.changelog_button.grid(
        row=0, column=2, padx=0, pady=0, sticky=tk.NSEW)
    tk_widgets.changelog_control = tk_widgets.bottom_widgets.changelog_button


def check_version():
    # read offline
    try:
        local_file = './version'
        with open(local_file, 'r') as f:
            global VERSION
            VERSION = f.read()
        title = f'LtMAO V{VERSION}'
        tk_widgets.main_tk.title(title)
        # read online
        remote_file = 'https://raw.githubusercontent.com/tarngaina/LtMAO/master/version'
        get = requests.get(remote_file)
        get.raise_for_status()
        global NEW_VERSION
        NEW_VERSION = get.text
        if VERSION != NEW_VERSION:
            title += f' - A new version has been out: {NEW_VERSION}, please redownload LtMAO to update it.'
        tk_widgets.main_tk.title(title) 
    except Exception as e:
        LOG(f'check_version: Failed: {e}')
    
    
def start():
    set_rce()
    create_main_app_and_frames()
    # load settings first
    setting.prepare(LOG)
    ctk.set_appearance_mode(setting.get('appearance','system'))
    set_style(setting.get('style', 'system'))
    set_theme(setting.get('theme', 'blue'))
    Log.limit = int(setting.get('Log.limit', '100'))
    
    # create UI
    create_page_controls()
    create_bottom_widgets()
    # select first page
    tk_widgets.select_control(0)
    # prepare
    cslmao.prepare(LOG)
    winLT.prepare(LOG)
    hash_manager.prepare(LOG)
    Thread(target=check_version, daemon=True).start()
    wad_tool.prepare(LOG)
    ext_tools.prepare(LOG)
    leaguefile_inspector.prepare(LOG)
    vo_helper.prepare(LOG)
    no_skin.prepare(LOG)
    uvee.prepare(LOG)
    shrum.prepare(LOG)
    hapiBin.prepare(LOG)
    pyntex.prepare(LOG)
    bnk_tool.prepare(LOG)
    sborf.prepare(LOG)
    lol2fbx.prepare(LOG)
    # loop the UI
    tk_widgets.main_tk.mainloop()
