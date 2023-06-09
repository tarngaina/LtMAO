
import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as tkfd

from LtMAO import setting, pyRitoFile, winLT, wad_tool, hash_manager, cslmao, leaguefile_inspector, animask_viewer, no_skin, vo_helper, uvee, ext_tools, shrum, pyntex, hapiBin, bnk_tool
from LtMAO.prettyUI.helper import Keeper, Log, EmojiImage

import os
import os.path
from threading import Thread
from traceback import format_exception
import datetime
from PIL import Image

LOG = Log.add
# transparent color
TRANSPARENT = 'transparent'
# to keep all created widgets
tk_widgets = Keeper()


def rce(self, *args):
    # redirect tkinter error print
    err = format_exception(*args)
    LOG(err)
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
    if os.path.exists(winLT.icon_file):
        tk_widgets.main_tk.iconbitmap(winLT.icon_file)
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


def create_CSLMAO_page():
    # create page frame
    tk_widgets.CSLMAO.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.CSLMAO.page_frame.columnconfigure(0, weight=1)
    tk_widgets.CSLMAO.page_frame.rowconfigure(0, weight=1)
    tk_widgets.CSLMAO.page_frame.rowconfigure(1, weight=699)
    # init stuffs
    tk_widgets.CSLMAO.mods = []
    tk_widgets.CSLMAO.make_overlay = None
    tk_widgets.CSLMAO.run_overlay = None
    # create action frame
    tk_widgets.CSLMAO.action_frame = ctk.CTkFrame(
        tk_widgets.CSLMAO.page_frame, fg_color=TRANSPARENT)
    tk_widgets.CSLMAO.action_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.CSLMAO.action_frame.rowconfigure(0, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(0, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(1, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(2, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(3, weight=699)
    tk_widgets.CSLMAO.action_frame.columnconfigure(4, weight=1)
    tk_widgets.CSLMAO.action_frame.columnconfigure(5, weight=1)

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
        image=EmojiImage.create('▶️', weird=True),
        command=run_cmd
    )
    tk_widgets.CSLMAO.run_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def import_cmd():
        if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
            return
        fantome_paths = tkfd.askopenfilenames(
            title='Import FANTOME',
            parent=tk_widgets.main_tk,
            filetypes=(('FANTOME/ZIP file', ('*.fantome', '*.zip')),),
            initialdir=setting.get('default_folder', None)
        )
        mgs = []
        for fantome_path in fantome_paths:
            mod_path = '.'.join(os.path.basename(fantome_path).split('.')[:-1])
            p = cslmao.import_fantome(fantome_path, mod_path)
            if p.returncode == 0:
                mod = cslmao.create_mod(
                    mod_path, False, tk_widgets.CSLMAO.get_mod_profile())
                info, image = cslmao.get_info(mod)
                mgs.append(add_mod(image=image, name=info['Name'], author=info['Author'],
                                   version=info['Version'], description=info['Description'], enable=mod.enable))
            LOG(f'cslmao: Imported: {fantome_path}')
        # grid after finish import
        for mg in mgs:
            mg()
        cslmao.save_mods()  # save outside loop

    # create import button
    tk_widgets.CSLMAO.import_button = ctk.CTkButton(
        tk_widgets.CSLMAO.action_frame,
        text='Import',
        image=EmojiImage.create('📄'),
        command=import_cmd
    )
    tk_widgets.CSLMAO.import_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def new_cmd():
        if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
            return
        mod_path = datetime.datetime.now().strftime(
            '%Y%m%d%H%M%S%f')
        mod = cslmao.create_mod(mod_path=mod_path, enable=False,
                                profile=tk_widgets.CSLMAO.get_mod_profile())
        cslmao.create_mod_folder(mod)
        cslmao.set_info(
            mod,
            info={
                'Name': 'New Mod',
                'Author': 'Author',
                'Version': '1.0',
                'Description': ''
            },
            image_path=None
        )
        add_mod(cslmao.CSLMAO.blank_image)()
    # create new button
    tk_widgets.CSLMAO.new_button = ctk.CTkButton(
        tk_widgets.CSLMAO.action_frame,
        text='New',
        image=EmojiImage.create('🆕'),
        command=new_cmd
    )
    tk_widgets.CSLMAO.new_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # create profile label
    tk_widgets.CSLMAO.profile_label = ctk.CTkLabel(
        tk_widgets.CSLMAO.action_frame,
        text='Profile: '
    )
    tk_widgets.CSLMAO.profile_label.grid(
        row=0, column=4, padx=5, pady=5, sticky=tk.NSEW)

    def profile_cmd(choice):
        tk_widgets.CSLMAO.refresh_profile(choice)
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
        command=profile_cmd
    )
    tk_widgets.CSLMAO.profile_opt.set(setting.get('Cslmao.profile', 'all'))
    tk_widgets.CSLMAO.profile_opt.grid(
        row=0, column=5, padx=5, pady=5, sticky=tk.NSEW)

    # create modlist frame
    tk_widgets.CSLMAO.modlist_frame = ctk.CTkScrollableFrame(
        tk_widgets.CSLMAO.page_frame)
    tk_widgets.CSLMAO.modlist_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.CSLMAO.modlist_frame.rowconfigure(0, weight=1)
    tk_widgets.CSLMAO.modlist_frame.columnconfigure(0, weight=1)

    # link tk add mod for cslmao
    def add_mod(image=None, name='New Mod', author='Author', version='1.0', description='', enable=False, profile='0'):
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
            if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
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
            text=f'{name} by {author} V{version}\n{description}'
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
                cslmao.CSLMAO.MODS[mod_id].path
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
            if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
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
            if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
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
                            cslmao.CSLMAO.MODS[mod_id].path
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
            image=EmojiImage.create('💾'),
            command=lambda: export_cmd(export_button)
        )
        export_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.NSEW)

        def remove_cmd(widget):
            if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
                return
            for mod_id, stuffs in enumerate(tk_widgets.CSLMAO.mods):
                if widget == stuffs[8]:
                    break
            tk_widgets.CSLMAO.mods.pop(mod_id)[0].destroy()
            cslmao.delete_mod(cslmao.CSLMAO.MODS.pop(mod_id))
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
        )
        name_entry.insert(0, name)
        name_entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        # create author entry
        author_entry = ctk.CTkEntry(
            edit_left_frame
        )
        author_entry.insert(0, author)
        author_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        # create version entry
        version_entry = ctk.CTkEntry(
            edit_left_frame
        )
        version_entry.insert(0, version)
        version_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
        # create description entry
        description_entry = ctk.CTkEntry(
            edit_left_frame
        )
        description_entry.insert(0, description)
        description_entry.grid(row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)
        edit_right_frame = ctk.CTkFrame(
            edit_frame
        )
        edit_right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        def edit_image_cmd(widget):
            if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
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
        )
        edit_profile_opt.set(profile)
        edit_profile_opt.grid(
            row=1, column=1, padx=20, pady=5, sticky=tk.NSEW)

        def reset_cmd(widget):
            if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
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
            command=lambda: reset_cmd(reset_button)
        )
        reset_button.grid(row=2, column=1, padx=20, pady=5, sticky=tk.NSEW)

        def save_cmd(widget):
            if tk_widgets.CSLMAO.make_overlay != None or tk_widgets.CSLMAO.run_overlay != None:
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
            tk_widgets.CSLMAO.mods[mod_id][12].configure(
                text=f'{info["Name"]} by {info["Author"]} V{info["Version"]}\n{info["Description"]}'
            )
            if image != None:
                tk_widgets.CSLMAO.mods[mod_id][13].configure(
                    image=ctk.CTkImage(Image.open(image), size=(144, 81))
                )
            mod.profile = tk_widgets.CSLMAO.mods[mod_id][19].get()
            cslmao.CSLMAO.save_mods()
            tk_widgets.CSLMAO.refresh_profile(
                setting.get('Cslmao.profile', 'all'))
        # create save button
        save_button = ctk.CTkButton(
            edit_action_frame,
            text='Save',
            image=EmojiImage.create('💾'),
            command=lambda: save_cmd(save_button)
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
        def mod_grid(id=id): return mod_frame.grid(
            row=id, column=0, padx=2, pady=2, sticky=tk.NSEW)
        return mod_grid

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

    def get_mod_profile():
        profile = setting.get('Cslmao.profile', 'all')
        if profile == 'all':
            return '0'
        else:
            return profile

    cslmao.tk_add_mod = add_mod
    tk_widgets.CSLMAO.refresh_profile = cslmao.tk_refresh_profile = refresh_profile
    tk_widgets.CSLMAO.get_mod_profile = get_mod_profile


def create_LFI_page():
    # create page frame
    tk_widgets.LFI.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.LFI.page_frame.columnconfigure(0, weight=1)
    tk_widgets.LFI.page_frame.rowconfigure(0, weight=1)
    tk_widgets.LFI.page_frame.rowconfigure(1, weight=699)
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
                False,  # deleted or not
                search_entry
            ]
        )

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
                    hash_manager.read_all_hashes()
                    for file_path in file_paths:
                        read_file(
                            file_path, hash_manager.HASHTABLES)
                    hash_manager.free_all_hashes()
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
        command=fileread_cmd
    )
    tk_widgets.LFI.fileread_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def folderread_cmd():
        if check_thread_safe(tk_widgets.LFI.reading_thread):
            dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Folder To Read',
                initialdir=setting.get('default_folder', None)
            )
            if dir_path != '':
                def folderread_thrd():
                    hash_manager.read_all_hashes()
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(
                                root, file).replace('\\', '/')
                            read_file(
                                file_path, hash_manager.HASHTABLES)
                    hash_manager.free_all_hashes()
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
        LOG(f'leaguefile_inspector: Done: Cleared all loaded files.')
    # create clear button
    tk_widgets.LFI.clear_button = ctk.CTkButton(
        tk_widgets.LFI.input_frame,
        text='Clear',
        image=EmojiImage.create('❌'),
        anchor=tk.CENTER,
        command=clear_cmd
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
        command=ritobin_cmd
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
        image=EmojiImage.create('📄'),
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
        image=EmojiImage.create('📄'),
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
        LOG('animask_viewer: Done: Load weight table')
    tk_widgets.AMV.load_button = ctk.CTkButton(
        tk_widgets.AMV.action_frame,
        text='Load',
        image=EmojiImage.create('🗿'),
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
        command=save_cmd
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
        command=clear_cmd
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
    tk_widgets.HM.info_frame.columnconfigure(0, weight=1)
    tk_widgets.HM.info_frame.columnconfigure(1, weight=0)
    tk_widgets.HM.info_frame.columnconfigure(2, weight=0)
    tk_widgets.HM.info_frame.columnconfigure(3, weight=699)
    tk_widgets.HM.info_frame.rowconfigure(0, weight=1)
    # create folder labels and folder buttons
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
    # create folder buttons
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
            image=EmojiImage.create('📂'),
            command=lambda index=i: folder_cmd(index)
        )
        folder_button.grid(row=i, column=1, padx=5,
                           pady=5, sticky=tk.NSEW)

    def reset_cmd():
        hash_manager.reset_custom_hashes(*hash_manager.ALL_HASHES)
        LOG('hash_manager: Done: Reset Custom Hashes to CDTB Hashes.')
    # create reset button
    reset_button = ctk.CTkButton(
        tk_widgets.HM.info_frame,
        text='Reset to CDTB hashes',
        image=EmojiImage.create('❌'),
        command=reset_cmd
    )
    reset_button.grid(row=2, column=2, padx=5, pady=5, sticky=tk.NSEW)

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
                    Log.tk_cooldown = 3000
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
        command=fileextract_cmd
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
                        Log.tk_cooldown = 3000
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
        command=folderextract_cmd
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
        text='Generate BIN hash:'
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
        text='->Entries',
        width=50,
        command=lambda: addbin_cmd('hashes.binentries.txt')
    )
    tk_widgets.HM.addentry_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.addfield_button = ctk.CTkButton(
        tk_widgets.HM.addbin_frame,
        text='->Fields',
        width=50,
        command=lambda: addbin_cmd('hashes.binfields.txt')
    )
    tk_widgets.HM.addfield_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.addtype_button = ctk.CTkButton(
        tk_widgets.HM.addbin_frame,
        text='->Types',
        width=50,
        command=lambda: addbin_cmd('hashes.bintypes.txt')
    )
    tk_widgets.HM.addtype_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.addhash_button = ctk.CTkButton(
        tk_widgets.HM.addbin_frame,
        text='->Hashes',
        width=50,
        command=lambda: addbin_cmd('hashes.binhashes.txt')
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
        wrap=tk.NONE
    )
    tk_widgets.HM.binraw_text.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.binraw_text.bind('<KeyRelease>', lambda event: binraw_cmd())
    # create bin hash text
    tk_widgets.HM.binhash_text = ctk.CTkTextbox(
        tk_widgets.HM.generate_frame,
        height=100,
        wrap=tk.NONE,
        state=tk.DISABLED
    )
    tk_widgets.HM.binhash_text.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create wad label
    tk_widgets.HM.wad_label = ctk.CTkLabel(
        tk_widgets.HM.generate_frame,
        text='Generate WAD hash:'
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
        text='->Game',
        width=50,
        command=lambda: addwad_cmd('hashes.game.txt')
    )
    tk_widgets.HM.addgame_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.addlcu_button = ctk.CTkButton(
        tk_widgets.HM.addwad_frame,
        text='->Lcu',
        width=50,
        command=lambda: addwad_cmd('hashes.lcu.txt')
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
        wrap=tk.NONE
    )
    tk_widgets.HM.wadraw_text.grid(
        row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HM.wadraw_text.bind('<KeyRelease>', lambda event: wadraw_cmd())
    # create wad hash text
    tk_widgets.HM.wadhash_text = ctk.CTkTextbox(
        tk_widgets.HM.generate_frame,
        height=100,
        wrap=tk.NONE,
        state=tk.DISABLED
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
    # init stuffs
    tk_widgets.VH.making_thread = None
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
    # create fantome entry
    tk_widgets.VH.fantome_entry = ctk.CTkEntry(
        tk_widgets.VH.input_frame
    )
    tk_widgets.VH.fantome_entry.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def browse_cmd():
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
            info, image, wads = vo_helper.scan_fantome(fantome_path)
            info_text = 'Info:\n'
            info_text += ''.join(f'{key}: {info[key]}\n' for key in info)
            info_text += '\nFiles:\n'
            info_text += 'META/info.json\n'
            if image:
                info_text += 'META/image.png\n'
            if len(wads) > 0:
                info_text += ''.join(f'{wad_name}\n' for wad_name in wads)

            tk_widgets.VH.info_text.configure(state=tk.NORMAL)
            tk_widgets.VH.info_text.delete('1.0', tk.END)
            tk_widgets.VH.info_text.insert(tk.END, info_text)
            tk_widgets.VH.info_text.configure(state=tk.DISABLED)
        tk_widgets.VH.fantome_entry.delete(0, tk.END)
        tk_widgets.VH.fantome_entry.insert(tk.END, fantome_path)

    # create browse button
    tk_widgets.VH.browse_button = ctk.CTkButton(
        tk_widgets.VH.input_frame,
        text='Browse FANTOME/ZIP',
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=browse_cmd
    )
    tk_widgets.VH.browse_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create info text
    tk_widgets.VH.info_text = ctk.CTkTextbox(
        tk_widgets.VH.page_frame,
        state=tk.DISABLED,
        wrap=tk.NONE
    )
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
        values=vo_helper.LANGS
    )
    tk_widgets.VH.target_option.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def taget_cmd():
        if not check_thread_safe(tk_widgets.VH.making_thread):
            LOG(
                'vo_helper: Failed: Remake Fantomes: A thread is already running, wait for it to finished.')
            return
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select Output Folder',
            initialdir=setting.get('default_folder', None)
        )
        if dir_path == '':
            return
        fantome_path = tk_widgets.VH.fantome_entry.get()
        fantome_name = os.path.basename(fantome_path)
        if fantome_path == '':
            return

        def make_thrd():
            LOG(f'vo_helper: Running: Remake FANTOME {fantome_path}')
            info, image, wads = vo_helper.read_fantome(fantome_path)
            vo_helper.make_fantome(
                fantome_name, dir_path, info, image, wads, [tk_widgets.VH.target_option.get()])

        tk_widgets.VH.making_thread = Thread(target=make_thrd, daemon=True)
        tk_widgets.VH.making_thread.start()

    # create target button
    tk_widgets.VH.target_button = ctk.CTkButton(
        tk_widgets.VH.action_frame,
        text='Remake For Selected Lang',
        image=EmojiImage.create('👌'),
        command=taget_cmd
    )
    tk_widgets.VH.target_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def make_cmd():
        if not check_thread_safe(tk_widgets.VH.making_thread):
            LOG(
                'vo_helper: Failed: Remake Fantomes: A thread is already running, wait for it to finished.')
            return
        dir_path = tkfd.askdirectory(
            parent=tk_widgets.main_tk,
            title='Select Output Folder',
            initialdir=setting.get('default_folder', None)
        )
        if dir_path == '':
            return
        fantome_path = tk_widgets.VH.fantome_entry.get()
        fantome_name = os.path.basename(fantome_path)
        if fantome_path == '':
            return

        def make_thrd():
            LOG(f'vo_helper: Running: Remake FANTOME {fantome_path}')
            info, image, wads = vo_helper.read_fantome(fantome_path)
            vo_helper.make_fantome(
                fantome_name, dir_path, info, image, wads, vo_helper.LANGS)

        tk_widgets.VH.making_thread = Thread(target=make_thrd, daemon=True)
        tk_widgets.VH.making_thread.start()

    # create make all button
    tk_widgets.VH.make_button = ctk.CTkButton(
        tk_widgets.VH.action_frame,
        text='Remake For All Langs',
        image=EmojiImage.create('👌'),
        command=make_cmd
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
        tk_widgets.NS.input_frame
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
        LOG('no_skin: Done: Save SKIPS.json')
    # create save SKIPS button
    tk_widgets.NS.save_skips_button = ctk.CTkButton(
        tk_widgets.NS.action_frame,
        text='Save SKIPS',
        image=EmojiImage.create('💾'),
        command=save_skips_cmd
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
        image=EmojiImage.create('🗿'),
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


def create_UVEE_page():
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
            for file_path in file_paths:
                read_file(file_path)
    # create file read button
    tk_widgets.UVEE.fileread_button = ctk.CTkButton(
        tk_widgets.UVEE.input_frame,
        text='Extract UVs From Files',
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=fileread_cmd
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
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(
                        root, file).replace('\\', '/')
                    read_file(file_path)
    # create folder read button
    tk_widgets.UVEE.folderread_button = ctk.CTkButton(
        tk_widgets.UVEE.input_frame,
        text='Extract UVs From Folder',
        image=EmojiImage.create('📁'),
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
        LOG(f'yvee: Done: Cleared all loaded images.')
    # create clear button
    tk_widgets.UVEE.clear_button = ctk.CTkButton(
        tk_widgets.UVEE.input_frame,
        text='Clear Loaded Images',
        image=EmojiImage.create('❌'),
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
        tk_widgets.SHR.input_frame
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
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=browsefile_cmd
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
        command=browsefolder_cmd
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
        wrap=tk.NONE
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
        text='Load joints from SKL',
        image=EmojiImage.create('📄'),
        command=old_skl_cmd
    )
    tk_widgets.SHR.old_skl_button.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    # create new textbox
    tk_widgets.SHR.new_text = ctk.CTkTextbox(
        tk_widgets.SHR.mid_frame,
        wrap=tk.NONE
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
        text='Load joints from SKL',
        image=EmojiImage.create('📄'),
        command=new_skl_cmd
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
        image=EmojiImage.create('✅'),
        command=rename_cmd
    )
    tk_widgets.SHR.rename_button.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

    def backup_cmd():
        setting.set('Shrum.backup', tk_widgets.SHR.backup_switch.get())
        setting.save()
    # create use ritobin switch
    tk_widgets.SHR.backup_switch = ctk.CTkSwitch(
        tk_widgets.SHR.action_frame,
        text='Create backup before rename (safe)',
        command=backup_cmd
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
    tk_widgets.HP.page_frame.rowconfigure(1, weight=699)
    # init stuffs
    tk_widgets.HP.working_thread = None
    # create input frame
    tk_widgets.HP.input_frame = ctk.CTkFrame(
        tk_widgets.HP.page_frame,
        fg_color=TRANSPARENT
    )
    tk_widgets.HP.input_frame.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HP.input_frame.columnconfigure(0, weight=9)
    tk_widgets.HP.input_frame.columnconfigure(1, weight=1)
    # create bin1 entry
    tk_widgets.HP.bin1_entry = ctk.CTkEntry(
        tk_widgets.HP.input_frame,
    )
    tk_widgets.HP.bin1_entry.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def bin1_cmd():
        skl_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.HP.bin1_entry.delete(0, tk.END)
        tk_widgets.HP.bin1_entry.insert(tk.END, skl_path)
    # create bin1 button
    tk_widgets.HP.bin1_button = ctk.CTkButton(
        tk_widgets.HP.input_frame,
        text='Browse BIN1',
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=bin1_cmd
    )
    tk_widgets.HP.bin1_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

    # create bin2 entry
    tk_widgets.HP.bin2_entry = ctk.CTkEntry(
        tk_widgets.HP.input_frame,
    )
    tk_widgets.HP.bin2_entry.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def bin2_cmd():
        skl_path = tkfd.askopenfilename(
            parent=tk_widgets.main_tk,
            title='Select BIN file',
            filetypes=(
                ('BIN files', '*.bin'),
                ('All files', '*.*'),
            ),
            initialdir=setting.get('default_folder', None)
        )
        tk_widgets.HP.bin2_entry.delete(0, tk.END)
        tk_widgets.HP.bin2_entry.insert(tk.END, skl_path)
    # create bin2 button
    tk_widgets.HP.bin2_button = ctk.CTkButton(
        tk_widgets.HP.input_frame,
        text='Browse BIN2',
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=bin2_cmd
    )
    tk_widgets.HP.bin2_button.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create action frame
    tk_widgets.HP.action_frame = ctk.CTkFrame(
        tk_widgets.HP.page_frame, fg_color=TRANSPARENT)
    tk_widgets.HP.action_frame.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.HP.action_frame.columnconfigure(0, weight=1)

    def hp_func(func_id):
        if check_thread_safe(tk_widgets.HP.working_thread):
            bin1 = tk_widgets.HP.bin1_entry.get()
            bin2 = tk_widgets.HP.bin2_entry.get()

            if func_id == 0:
                if bin1 != '' and bin2 != '':
                    def working_thrd():
                        hapiBin.copy_linked_list(bin2, bin1)
                    tk_widgets.HP.working_thread = Thread(
                        target=working_thrd, daemon=True
                    )
                    tk_widgets.HP.working_thread.start()

            elif func_id == 1:
                if bin1 != '' and bin2 != '':
                    def working_thrd():
                        hapiBin.copy_vfx_colors(bin2, bin1)
                    tk_widgets.HP.working_thread = Thread(
                        target=working_thrd, daemon=True
                    )
                    tk_widgets.HP.working_thread.start()
        else:
            LOG(
                'hapiBin: Failed: A thread is already running, wait for it to finished.')

    # init funcs
    hp_funcs = [
        {
            'name': 'Copy Linked List from BIN2 to BIN1',
            'desc': 'Copy linked list.',
            'func': lambda: hp_func(0),
            'icon': EmojiImage.create('🔗')
        },
        {
            'name': 'Copy VFX colors from BIN2 to BIN1',
            'desc': 'Copy color, birthColor, reflectionDefinition, lingerColor of VfxEmitterDefinitionData.\nCopy colors, mColorOn, mColorOff of StaticMaterialShaderParamDef/DynamicMaterialParameterDef.',
            'func': lambda: hp_func(1),
            'icon': EmojiImage.create('🎨')
        }
    ]
    # create hp funcs
    for func_id, func in enumerate(hp_funcs):
        func_frame = ctk.CTkFrame(
            tk_widgets.HP.action_frame
        )
        func_frame.grid(row=func_id, column=0, padx=5, pady=5, sticky=tk.NSEW)
        tk_widgets.HP.action_frame.rowconfigure(func_id, weight=1)
        func_frame.rowconfigure(0, weight=1)
        func_frame.rowconfigure(1, weight=1)
        func_frame.columnconfigure(0, weight=1)
        func_button = ctk.CTkButton(
            func_frame,
            text=func['name'],
            command=func['func'],
            image=func['icon']
        )
        func_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NS+tk.W)
        func_label = ctk.CTkLabel(
            func_frame,
            text=func['desc'],
            anchor=tk.W,
            justify=tk.LEFT
        )
        func_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NS+tk.W)
    tk_widgets.HP.action_frame.rowconfigure(len(hp_funcs), weight=699)


def create_WT_page():
    # create page frame
    tk_widgets.WT.page_frame = ctk.CTkFrame(
        tk_widgets.mainright_frame,
        fg_color=TRANSPARENT,
    )
    tk_widgets.WT.page_frame.columnconfigure(0, weight=1)
    tk_widgets.WT.page_frame.rowconfigure(0, weight=1)
    tk_widgets.WT.page_frame.rowconfigure(1, weight=699)
    # init stuffs
    tk_widgets.WT.working_thread = None
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
                    for file_path in file_paths:
                        src = file_path
                        dst = src.replace('.wad.client', '.wad')
                        Log.tk_cooldown = 3000
                        wad_tool.unpack(src, dst)
                        Log.tk_cooldown = 0
                        LOG(
                            f'wad_tool: Done: Unpack {src}')
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
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=wad2dir_cmd
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
                    Log.tk_cooldown = 3000
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
        command=dir2wad_cmd
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
        text='Bulk unpack WADs to same Folder'
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
    tk_widgets.WT.action3_frame.columnconfigure(2, weight=699)

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
            tk_widgets.WT.file_text.configure(state=tk.NORMAL)
            tk_widgets.WT.file_text.insert(tk.END, '\n'.join(file_paths))
            tk_widgets.WT.file_text.configure(state=tk.DISABLED)

    # create add file button
    tk_widgets.WT.addfile_button = ctk.CTkButton(
        tk_widgets.WT.action3_frame,
        text='Add Files',
        image=EmojiImage.create('📄'),
        command=addfile_cmd
    )
    tk_widgets.WT.addfile_button.grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def clear_cmd():
        tk_widgets.WT.file_text.configure(state=tk.NORMAL)
        tk_widgets.WT.file_text.delete('1.0', tk.END)
        tk_widgets.WT.file_text.configure(state=tk.DISABLED)
    # create clear button
    tk_widgets.WT.clear_button = ctk.CTkButton(
        tk_widgets.WT.action3_frame,
        text='Clear',
        image=EmojiImage.create('❌'),
        command=clear_cmd
    )
    tk_widgets.WT.clear_button.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # create file text
    tk_widgets.WT.file_text = ctk.CTkTextbox(
        tk_widgets.WT.action2_frame,
        wrap=tk.NONE,
        state=tk.DISABLED
    )
    tk_widgets.WT.file_text.grid(
        row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def bulk_cmd():
        if check_thread_safe(tk_widgets.WT.working_thread):
            dir_path = tkfd.askdirectory(
                parent=tk_widgets.main_tk,
                title='Select Output Folder',
                initialdir=setting.get('default_folder', None)
            )
            if dir_path != '':
                file_paths = tk_widgets.WT.file_text.get(
                    '1.0', 'end-1c').split('\n')
                if len(file_paths) > 0:
                    def working_thrd():
                        Log.tk_cooldown = 3000
                        for file_path in file_paths:
                            wad_tool.unpack(file_path, dir_path)
                        Log.tk_cooldown = 0
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
        command=bulk_cmd
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
        image=EmojiImage.create('📄'),
        anchor=tk.CENTER,
        command=parsewad_cmd
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
        command=parsedir_cmd
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
        wrap=tk.NONE,
        state=tk.DISABLED,
        border_spacing=10
    )
    tk_widgets.LOG.log_textbox.grid(row=0, column=0, sticky=tk.NSEW)
    Log.tk_log = tk_widgets.LOG.log_textbox


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
        text='General'
    )
    tk_widgets.ST.general_label.grid(
        row=0, column=0, padx=10, pady=5, sticky=tk.NSEW)
    # theme
    tk_widgets.ST.theme_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Theme:',
        image=EmojiImage.create('🖌️', weird=True),
        compound=tk.LEFT,
        anchor=tk.W
    )
    tk_widgets.ST.theme_label.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

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
        row=1, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # limit message
    tk_widgets.ST.loglimit_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Log Limit Messages:',
        image=EmojiImage.create('🗒️', weird=True),
        compound=tk.LEFT,
        anchor=tk.W
    )
    tk_widgets.ST.loglimit_label.grid(
        row=2, column=1, padx=5, pady=5, sticky=tk.NSEW)

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
        row=2, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # shortcut desktop
    tk_widgets.ST.desktop_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Create Desktop Shortcut',
        image=EmojiImage.create('🖥️', weird=True),
        anchor=tk.W,
        command=winLT.Shortcut.create_desktop
    )
    tk_widgets.ST.desktop_button.grid(
        row=3, column=1, padx=5, pady=5, sticky=tk.NSEW)
    # explorer context
    tk_widgets.ST.contextadd_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Create Explorer Contexts',
        image=EmojiImage.create('💬'),
        anchor=tk.W,
        command=winLT.Context.create_contexts
    )
    tk_widgets.ST.contextadd_button.grid(
        row=4, column=1, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.ST.contextrmv_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Remove Explorer Contexts',
        image=EmojiImage.create('❌'),
        anchor=tk.W,
        command=winLT.Context.remove_contexts
    )
    tk_widgets.ST.contextrmv_button.grid(
        row=4, column=2, padx=5, pady=5, sticky=tk.NSEW)
    # default folder
    tk_widgets.ST.defaultdir_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Default Folder:',
        image=EmojiImage.create('🌳'),
        compound=tk.LEFT,
        anchor=tk.W
    )
    tk_widgets.ST.defaultdir_label.grid(
        row=6, column=1, padx=5, pady=5, sticky=tk.NSEW)

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
        command=defaultdir_cmd
    )
    tk_widgets.ST.defaultdir_button.grid(
        row=6, column=2, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.ST.defaultdir_value_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        anchor=tk.W
    )
    defaultdir = setting.get('default_dir', None)
    if defaultdir == None:
        tk_widgets.ST.defaultdir_value_label.configure(
            text='Default folder for all ask-file/ask-folder dialog'
        )
    tk_widgets.ST.defaultdir_value_label.grid(
        row=6, column=3, padx=5, pady=5, sticky=tk.NSEW)
    # cslmao label
    tk_widgets.ST.cslmao_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='CSLMAO'
    )
    tk_widgets.ST.cslmao_label.grid(
        row=7, column=0, padx=10, pady=5, sticky=tk.NSEW)
    # game folder
    tk_widgets.ST.gamedir_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Game Folder:',
        image=EmojiImage.create('🎮'),
        compound=tk.LEFT,
        anchor=tk.W
    )
    tk_widgets.ST.gamedir_label.grid(
        row=8, column=1, padx=5, pady=5, sticky=tk.NSEW)

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
            tk_widgets.ST.gamedir_value_label.configure(text=dir_path)
    tk_widgets.ST.gamedir_button = ctk.CTkButton(
        tk_widgets.ST.scroll_frame,
        text='Browse',
        image=EmojiImage.create('📁'),
        command=gamedir_cmd
    )
    tk_widgets.ST.gamedir_button.grid(
        row=8, column=2, padx=5, pady=5, sticky=tk.NSEW)
    tk_widgets.ST.gamedir_value_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text=setting.get(
            'game_folder', 'Please choose League of Legends/Game folder.'),
        anchor=tk.W
    )
    tk_widgets.ST.gamedir_value_label.grid(
        row=8, column=3, padx=5, pady=5, sticky=tk.NSEW)
    # extra game modes
    tk_widgets.ST.egm_label = ctk.CTkLabel(
        tk_widgets.ST.scroll_frame,
        text='Extra Game Modes:',
        image=EmojiImage.create('🕹️', weird=True),
        compound=tk.LEFT,
        anchor=tk.W
    )
    tk_widgets.ST.egm_label.grid(
        row=9, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def egm_cmd():
        setting.set('Cslmao.extra_game_modes',
                    tk_widgets.ST.egm_checkbox.get())
        setting.save()
    tk_widgets.ST.egm_checkbox = ctk.CTkCheckBox(
        tk_widgets.ST.scroll_frame,
        text='',
        command=egm_cmd
    )
    if setting.get('Cslmao.extra_game_modes', 0) == 1:
        tk_widgets.ST.egm_checkbox.select()
    else:
        tk_widgets.ST.egm_checkbox.deselect()
    tk_widgets.ST.egm_checkbox.grid(
        row=9, column=2, padx=5, pady=5, sticky=tk.NSEW)


def select_right_page(selected):
    # hide all page
    for page in tk_widgets.pages:
        if page.page_frame != None:
            page.page_frame.grid_forget()
    tk_widgets.ST.page_frame.grid_forget()
    tk_widgets.LOG.page_frame.grid_forget()
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
    else:
        # setting page
        tk_widgets.ST.page_frame.grid(
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
        else:
            # setting control
            tk_widgets.setting_control.configure(
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
            text='shrum',
            command=lambda: control_cmd(7)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='hapiBin',
            command=lambda: control_cmd(8)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='wad_tool',
            command=lambda: control_cmd(9)
        ),
        ctk.CTkButton(
            tk_widgets.mainleft_frame,
            text='pyntex',
            command=lambda: control_cmd(10)
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
        create_PT_page
    ]
    # create LOG and ST control, page
    tk_widgets.minilog_control = None
    tk_widgets.setting_control = None
    tk_widgets.LOG = Keeper()
    tk_widgets.ST = Keeper()
    create_LOG_page()
    create_ST_page()


def create_bottom_widgets():
    tk_widgets.mainbottom_frame.columnconfigure(0, weight=1)
    tk_widgets.mainbottom_frame.columnconfigure(1, weight=0)
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
        width=30,
        text='',
        image=EmojiImage.create('⚙️', weird=True),
        command=lambda: tk_widgets.select_control(1000)
    )
    tk_widgets.bottom_widgets.setting_button.grid(
        row=0, column=1, padx=(0, 5), pady=0, sticky=tk.NSEW)
    tk_widgets.setting_control = tk_widgets.bottom_widgets.setting_button


def start():
    create_main_app_and_frames()
    # load settings first
    setting.prepare(LOG)
    ctk.set_appearance_mode(setting.get('theme', 'system'))
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
    # loop the UI
    tk_widgets.main_tk.mainloop()
