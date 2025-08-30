"""
f3d library bindings
"""
from __future__ import annotations
import os
import typing
__all__ = ['Camera', 'CameraState', 'Engine', 'Image', 'InteractionBind', 'Interactor', 'LibInformation', 'Log', 'Mesh', 'Options', 'ReaderInformation', 'Scene', 'Utils', 'Window']
class Camera:
    focal_point: tuple[float, float, float]
    position: tuple[float, float, float]
    state: CameraState
    view_angle: float
    view_up: tuple[float, float, float]
    def azimuth(self, arg0: float) -> Camera:
        ...
    def dolly(self, arg0: float) -> Camera:
        ...
    def elevation(self, arg0: float) -> Camera:
        ...
    def pan(self, right: float, up: float, forward: float = 0.0) -> Camera:
        ...
    def pitch(self, arg0: float) -> Camera:
        ...
    def reset_to_bounds(self, zoom_factor: float = 0.9) -> Camera:
        ...
    def reset_to_default(self) -> Camera:
        ...
    def roll(self, arg0: float) -> Camera:
        ...
    def set_current_as_default(self) -> Camera:
        ...
    def yaw(self, arg0: float) -> Camera:
        ...
    def zoom(self, arg0: float) -> Camera:
        ...
class CameraState:
    focal_point: tuple[float, float, float]
    position: tuple[float, float, float]
    view_angle: float
    view_up: tuple[float, float, float]
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, position: tuple[float, float, float] = (0.0, 0.0, 1.0), focal_point: tuple[float, float, float] = (0.0, 0.0, 0.0), view_up: tuple[float, float, float] = (0.0, 1.0, 0.0), view_angle: float = 30.0) -> None:
        ...
class Engine:
    options: Options
    @staticmethod
    def autoload_plugins() -> None:
        """
        Automatically load internal plugins
        """
    @staticmethod
    def create(offscreen: bool = False) -> Engine:
        """
        Create an engine with a automatic window
        """
    @staticmethod
    def create_egl() -> Engine:
        """
        Create an engine with an EGL window (Windows/Linux only)
        """
    @staticmethod
    def create_external_cocoa() -> Engine:
        """
        Create an engine with an existing COCOA context (macOS only)
        """
    @staticmethod
    def create_external_egl() -> Engine:
        """
        Create an engine with an existing EGL context (Windows/Linux only)
        """
    @staticmethod
    def create_external_glx() -> Engine:
        """
        Create an engine with an existing GLX context (Linux only)
        """
    @staticmethod
    def create_external_osmesa() -> Engine:
        """
        Create an engine with an existing OSMesa context (Windows/Linux only)
        """
    @staticmethod
    def create_external_wgl() -> Engine:
        """
        Create an engine with an existing WGL context (Windows only)
        """
    @staticmethod
    def create_glx(arg0: bool) -> Engine:
        """
        Create an engine with an GLX window (Linux only)
        """
    @staticmethod
    def create_none() -> Engine:
        """
        Create an engine with no window
        """
    @staticmethod
    def create_osmesa() -> Engine:
        """
        Create an engine with an OSMesa window (Windows/Linux only)
        """
    @staticmethod
    def create_wgl(arg0: bool) -> Engine:
        """
        Create an engine with an WGL window (Windows only)
        """
    @staticmethod
    def get_all_reader_option_names() -> list[str]:
        ...
    @staticmethod
    def get_lib_info() -> LibInformation:
        ...
    @staticmethod
    def get_plugins_list(arg0: os.PathLike[str]) -> list[str]:
        ...
    @staticmethod
    def get_readers_info() -> list[ReaderInformation]:
        ...
    @staticmethod
    def get_rendering_backend_list() -> dict[str, bool]:
        ...
    @staticmethod
    def load_plugin(arg0: str, arg1: typing.Sequence[os.PathLike[str]]) -> None:
        """
        Load a plugin
        """
    @staticmethod
    def set_reader_option(arg0: str, arg1: str) -> None:
        ...
    def set_cache_path(self, arg0: os.PathLike[str]) -> Engine:
        """
        Set the cache path directory
        """
    @property
    def interactor(self) -> Interactor:
        ...
    @property
    def scene(self) -> Scene:
        ...
    @property
    def window(self) -> Window:
        ...
class Image:
    class ChannelType:
        """
        Members:
        
          BYTE
        
          SHORT
        
          FLOAT
        """
        BYTE: typing.ClassVar[Image.ChannelType]  # value = <ChannelType.BYTE: 0>
        FLOAT: typing.ClassVar[Image.ChannelType]  # value = <ChannelType.FLOAT: 2>
        SHORT: typing.ClassVar[Image.ChannelType]  # value = <ChannelType.SHORT: 1>
        __members__: typing.ClassVar[dict[str, Image.ChannelType]]  # value = {'BYTE': <ChannelType.BYTE: 0>, 'SHORT': <ChannelType.SHORT: 1>, 'FLOAT': <ChannelType.FLOAT: 2>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class SaveFormat:
        """
        Members:
        
          PNG
        
          JPG
        
          TIF
        
          BMP
        """
        BMP: typing.ClassVar[Image.SaveFormat]  # value = <SaveFormat.BMP: 3>
        JPG: typing.ClassVar[Image.SaveFormat]  # value = <SaveFormat.JPG: 1>
        PNG: typing.ClassVar[Image.SaveFormat]  # value = <SaveFormat.PNG: 0>
        TIF: typing.ClassVar[Image.SaveFormat]  # value = <SaveFormat.TIF: 2>
        __members__: typing.ClassVar[dict[str, Image.SaveFormat]]  # value = {'PNG': <SaveFormat.PNG: 0>, 'JPG': <SaveFormat.JPG: 1>, 'TIF': <SaveFormat.TIF: 2>, 'BMP': <SaveFormat.BMP: 3>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    BMP: typing.ClassVar[Image.SaveFormat]  # value = <SaveFormat.BMP: 3>
    BYTE: typing.ClassVar[Image.ChannelType]  # value = <ChannelType.BYTE: 0>
    FLOAT: typing.ClassVar[Image.ChannelType]  # value = <ChannelType.FLOAT: 2>
    JPG: typing.ClassVar[Image.SaveFormat]  # value = <SaveFormat.JPG: 1>
    PNG: typing.ClassVar[Image.SaveFormat]  # value = <SaveFormat.PNG: 0>
    SHORT: typing.ClassVar[Image.ChannelType]  # value = <ChannelType.SHORT: 1>
    TIF: typing.ClassVar[Image.SaveFormat]  # value = <SaveFormat.TIF: 2>
    __hash__: typing.ClassVar[None] = None
    content: bytes
    @staticmethod
    def supported_formats() -> list[str]:
        ...
    def __eq__(self, arg0: Image) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: os.PathLike[str]) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: int, arg1: int, arg2: int, arg3: Image.ChannelType) -> None:
        ...
    def __ne__(self, arg0: Image) -> bool:
        ...
    def _repr_png_(self) -> bytes:
        ...
    def all_metadata(self) -> list[str]:
        ...
    def compare(self, arg0: Image) -> float:
        ...
    def get_metadata(self, arg0: str) -> str:
        ...
    def normalized_pixel(self, arg0: tuple[int, int]) -> list[float]:
        ...
    def save(self, path: os.PathLike[str], format: Image.SaveFormat = Image.SaveFormat.PNG) -> Image:
        ...
    def save_buffer(self, format: Image.SaveFormat = Image.SaveFormat.PNG) -> bytes:
        ...
    def set_metadata(self, arg0: str, arg1: str) -> Image:
        ...
    def to_terminal_text(self) -> str:
        ...
    @property
    def channel_count(self) -> int:
        ...
    @property
    def channel_type(self) -> Image.ChannelType:
        ...
    @property
    def channel_type_size(self) -> int:
        ...
    @property
    def height(self) -> int:
        ...
    @property
    def width(self) -> int:
        ...
class InteractionBind:
    class ModifierKeys:
        """
        Members:
        
          ANY
        
          NONE
        
          CTRL
        
          SHIFT
        
          CTRL_SHIFT
        """
        ANY: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.ANY: 128>
        CTRL: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.CTRL: 1>
        CTRL_SHIFT: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.CTRL_SHIFT: 3>
        NONE: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.NONE: 0>
        SHIFT: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.SHIFT: 2>
        __members__: typing.ClassVar[dict[str, InteractionBind.ModifierKeys]]  # value = {'ANY': <ModifierKeys.ANY: 128>, 'NONE': <ModifierKeys.NONE: 0>, 'CTRL': <ModifierKeys.CTRL: 1>, 'SHIFT': <ModifierKeys.SHIFT: 2>, 'CTRL_SHIFT': <ModifierKeys.CTRL_SHIFT: 3>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    ANY: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.ANY: 128>
    CTRL: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.CTRL: 1>
    CTRL_SHIFT: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.CTRL_SHIFT: 3>
    NONE: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.NONE: 0>
    SHIFT: typing.ClassVar[InteractionBind.ModifierKeys]  # value = <ModifierKeys.SHIFT: 2>
    inter: str
    mod: InteractionBind.ModifierKeys
    def __init__(self, arg0: InteractionBind.ModifierKeys, arg1: str) -> None:
        ...
    def format(self) -> str:
        ...
class Interactor:
    @typing.overload
    def add_binding(self, arg0: InteractionBind, arg1: str, arg2: str, arg3: typing.Callable[[], tuple[str, str]]) -> Interactor:
        """
        Add a binding command
        """
    @typing.overload
    def add_binding(self, arg0: InteractionBind, arg1: typing.Sequence[str], arg2: str, arg3: typing.Callable[[], tuple[str, str]]) -> Interactor:
        """
        Add binding commands
        """
    def add_command(self, arg0: str, arg1: typing.Callable[[list[str]], None]) -> Interactor:
        """
        Add a command
        """
    def disable_camera_movement(self) -> Interactor:
        """
        Disable the camera interaction
        """
    def enable_camera_movement(self) -> Interactor:
        """
        Enable the camera interaction
        """
    def get_bind_groups(self) -> list[str]:
        ...
    def get_binding_documentation(self, arg0: InteractionBind) -> tuple[str, str]:
        ...
    def get_binds(self) -> list[InteractionBind]:
        ...
    def get_binds_for_group(self, arg0: str) -> list[InteractionBind]:
        ...
    def get_command_actions(self) -> list[str]:
        """
        Get all command actions
        """
    def init_bindings(self) -> Interactor:
        """
        Remove all bindings and add default bindings
        """
    def init_commands(self) -> Interactor:
        """
        Remove all commands and add all default command callbacks
        """
    def is_playing_animation(self) -> bool:
        """
        Returns True if the animation is currently started
        """
    def play_interaction(self, arg0: os.PathLike[str], arg1: float, arg2: typing.Callable[[], None]) -> bool:
        """
        Play an interaction file
        """
    def record_interaction(self, arg0: os.PathLike[str]) -> bool:
        """
        Record an interaction file
        """
    def remove_binding(self, arg0: InteractionBind) -> Interactor:
        """
        Remove interaction commands
        """
    def remove_command(self, arg0: str) -> Interactor:
        """
        Remove a command
        """
    def request_render(self) -> Interactor:
        """
        Request a render on the next event loop
        """
    def start(self, delta_time: float = 0.03333333333333333, user_callback: typing.Callable[[], None] = None) -> Interactor:
        """
        Start the interactor and the event loop
        """
    def start_animation(self) -> Interactor:
        """
        Start the animation
        """
    def stop(self) -> Interactor:
        """
        Stop the interactor and the event loop
        """
    def stop_animation(self) -> Interactor:
        """
        Stop the animation
        """
    def toggle_animation(self) -> Interactor:
        """
        Toggle the animation
        """
    def trigger_command(self, arg0: str) -> bool:
        """
        Trigger a command
        """
class LibInformation:
    @property
    def build_date(self) -> str:
        ...
    @property
    def build_system(self) -> str:
        ...
    @property
    def compiler(self) -> str:
        ...
    @property
    def copyrights(self) -> list[str]:
        ...
    @property
    def license(self) -> str:
        ...
    @property
    def modules(self) -> dict[str, bool]:
        ...
    @property
    def version(self) -> str:
        ...
    @property
    def version_full(self) -> str:
        ...
    @property
    def vtk_version(self) -> str:
        ...
class Log:
    class VerboseLevel:
        """
        Members:
        
          DEBUG
        
          INFO
        
          WARN
        
          ERROR
        
          QUIET
        """
        DEBUG: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.DEBUG: 0>
        ERROR: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.ERROR: 3>
        INFO: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.INFO: 1>
        QUIET: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.QUIET: 4>
        WARN: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.WARN: 2>
        __members__: typing.ClassVar[dict[str, Log.VerboseLevel]]  # value = {'DEBUG': <VerboseLevel.DEBUG: 0>, 'INFO': <VerboseLevel.INFO: 1>, 'WARN': <VerboseLevel.WARN: 2>, 'ERROR': <VerboseLevel.ERROR: 3>, 'QUIET': <VerboseLevel.QUIET: 4>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    DEBUG: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.DEBUG: 0>
    ERROR: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.ERROR: 3>
    INFO: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.INFO: 1>
    QUIET: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.QUIET: 4>
    WARN: typing.ClassVar[Log.VerboseLevel]  # value = <VerboseLevel.WARN: 2>
    @staticmethod
    def get_verbose_level() -> Log.VerboseLevel:
        ...
    @staticmethod
    def print(arg0: Log.VerboseLevel, arg1: str) -> None:
        ...
    @staticmethod
    def set_use_coloring(arg0: bool) -> None:
        ...
    @staticmethod
    def set_verbose_level(level: Log.VerboseLevel, force_std_err: bool = False) -> None:
        ...
class Mesh:
    face_indices: list[int]
    face_sides: list[int]
    normals: list[float]
    points: list[float]
    texture_coordinates: list[float]
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, points: typing.Sequence[float], normals: typing.Sequence[float] = [], texture_coordinates: typing.Sequence[float] = [], face_sides: typing.Sequence[int] = [], face_indices: typing.Sequence[int] = []) -> None:
        ...
class Options:
    def __getitem__(self, arg0: str) -> bool | int | float | str | list[float] | list[int]:
        ...
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator[typing.Any]:
        ...
    def __len__(self) -> int:
        ...
    def __setitem__(self, arg0: str, arg1: bool | int | float | str | typing.Sequence[float] | typing.Sequence[int]) -> None:
        ...
    def copy(self, arg0: Options, arg1: str) -> Options:
        ...
    def get_closest_option(self, arg0: str) -> tuple[str, int]:
        ...
    def is_same(self, arg0: Options, arg1: str) -> bool:
        ...
    def keys(self) -> list[str]:
        ...
    def toggle(self, arg0: str) -> Options:
        ...
    def update(self, arg: typing.Union[typing.Mapping[str, typing.Any], typing.Iterable[tuple[str, typing.Any]]]) -> None:
        ...
class ReaderInformation:
    @property
    def description(self) -> str:
        ...
    @property
    def extensions(self) -> list[str]:
        ...
    @property
    def has_geometry_reader(self) -> bool:
        ...
    @property
    def has_scene_reader(self) -> bool:
        ...
    @property
    def mime_types(self) -> list[str]:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def plugin_name(self) -> str:
        ...
class Scene:
    @typing.overload
    def add(self, file_path: os.PathLike[str]) -> Scene:
        """
        Add a file the scene
        """
    @typing.overload
    def add(self, file_path_vector: typing.Sequence[os.PathLike[str]]) -> Scene:
        """
        Add multiple filepaths to the scene
        """
    @typing.overload
    def add(self, file_name_vector: typing.Sequence[str]) -> Scene:
        """
        Add multiple filenames to the scene
        """
    @typing.overload
    def add(self, mesh: Mesh) -> Scene:
        """
        Add a surfacic mesh from memory into the scene
        """
    def animation_time_range(self) -> tuple[float, float]:
        ...
    def available_animations(self) -> int:
        ...
    def clear(self) -> Scene:
        ...
    def load_animation_time(self, arg0: float) -> Scene:
        ...
    def supports(self, arg0: os.PathLike[str]) -> bool:
        ...
class Utils:
    class KnownFolder:
        """
        Members:
        
          ROAMINGAPPDATA
        
          LOCALAPPDATA
        
          PICTURES
        """
        LOCALAPPDATA: typing.ClassVar[Utils.KnownFolder]  # value = <KnownFolder.LOCALAPPDATA: 1>
        PICTURES: typing.ClassVar[Utils.KnownFolder]  # value = <KnownFolder.PICTURES: 2>
        ROAMINGAPPDATA: typing.ClassVar[Utils.KnownFolder]  # value = <KnownFolder.ROAMINGAPPDATA: 0>
        __members__: typing.ClassVar[dict[str, Utils.KnownFolder]]  # value = {'ROAMINGAPPDATA': <KnownFolder.ROAMINGAPPDATA: 0>, 'LOCALAPPDATA': <KnownFolder.LOCALAPPDATA: 1>, 'PICTURES': <KnownFolder.PICTURES: 2>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    LOCALAPPDATA: typing.ClassVar[Utils.KnownFolder]  # value = <KnownFolder.LOCALAPPDATA: 1>
    PICTURES: typing.ClassVar[Utils.KnownFolder]  # value = <KnownFolder.PICTURES: 2>
    ROAMINGAPPDATA: typing.ClassVar[Utils.KnownFolder]  # value = <KnownFolder.ROAMINGAPPDATA: 0>
    @staticmethod
    def collapse_path(arg0: os.PathLike[str], arg1: os.PathLike[str]) -> os.PathLike[str]:
        ...
    @staticmethod
    def get_env(arg0: str) -> str | None:
        ...
    @staticmethod
    def get_known_folder(arg0: Utils.KnownFolder) -> str | None:
        ...
    @staticmethod
    def glob_to_regex(glob: str, path_separator: str = '/') -> str:
        ...
    @staticmethod
    def text_distance(arg0: str, arg1: str) -> int:
        ...
class Window:
    class Type:
        """
        Members:
        
          NONE
        
          EXTERNAL
        
          GLX
        
          WGL
        
          COCOA
        
          EGL
        
          OSMESA
        
          UNKNOWN
        """
        COCOA: typing.ClassVar[Window.Type]  # value = <Type.COCOA: 4>
        EGL: typing.ClassVar[Window.Type]  # value = <Type.EGL: 5>
        EXTERNAL: typing.ClassVar[Window.Type]  # value = <Type.EXTERNAL: 1>
        GLX: typing.ClassVar[Window.Type]  # value = <Type.GLX: 2>
        NONE: typing.ClassVar[Window.Type]  # value = <Type.NONE: 0>
        OSMESA: typing.ClassVar[Window.Type]  # value = <Type.OSMESA: 6>
        UNKNOWN: typing.ClassVar[Window.Type]  # value = <Type.UNKNOWN: 8>
        WGL: typing.ClassVar[Window.Type]  # value = <Type.WGL: 3>
        __members__: typing.ClassVar[dict[str, Window.Type]]  # value = {'NONE': <Type.NONE: 0>, 'EXTERNAL': <Type.EXTERNAL: 1>, 'GLX': <Type.GLX: 2>, 'WGL': <Type.WGL: 3>, 'COCOA': <Type.COCOA: 4>, 'EGL': <Type.EGL: 5>, 'OSMESA': <Type.OSMESA: 6>, 'UNKNOWN': <Type.UNKNOWN: 8>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    COCOA: typing.ClassVar[Window.Type]  # value = <Type.COCOA: 4>
    EGL: typing.ClassVar[Window.Type]  # value = <Type.EGL: 5>
    EXTERNAL: typing.ClassVar[Window.Type]  # value = <Type.EXTERNAL: 1>
    GLX: typing.ClassVar[Window.Type]  # value = <Type.GLX: 2>
    NONE: typing.ClassVar[Window.Type]  # value = <Type.NONE: 0>
    OSMESA: typing.ClassVar[Window.Type]  # value = <Type.OSMESA: 6>
    UNKNOWN: typing.ClassVar[Window.Type]  # value = <Type.UNKNOWN: 8>
    WGL: typing.ClassVar[Window.Type]  # value = <Type.WGL: 3>
    height: int
    size: tuple[int, int]
    width: int
    def get_display_from_world(self, arg0: tuple[float, float, float]) -> tuple[float, float, float]:
        """
        Get display coordinate point from world coordinate
        """
    def get_world_from_display(self, arg0: tuple[float, float, float]) -> tuple[float, float, float]:
        """
        Get world coordinate point from display coordinate
        """
    def render(self) -> bool:
        """
        Render the window
        """
    def render_to_image(self, no_background: bool = False) -> Image:
        """
        Render the window to an image
        """
    def set_icon(self, arg0: int, arg1: int) -> Window:
        """
        Set the icon of the window using a memory buffer representing a PNG file
        """
    def set_position(self, arg0: int, arg1: int) -> Window:
        ...
    def set_window_name(self, arg0: str) -> Window:
        """
        Set the window name
        """
    @property
    def camera(self) -> Camera:
        ...
    @property
    def offscreen(self) -> bool:
        ...
    @property
    def type(self) -> Window.Type:
        ...
