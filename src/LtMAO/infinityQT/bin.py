from PySide6.QtWidgets import QWidget, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QLineEdit, QHeaderView, QComboBox, QLabel
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Qt

from .. import lepath, pyRitoFile, hash_helper

all_bin_types = [member.name.lower() for member in pyRitoFile.bin.BINType]

def build_links(treewidget: QTreeWidget, links):
    links_item = QTreeWidgetItem(treewidget)
    links_item.setText(0, 'Links')
    for link in links:
        link_item = QTreeWidgetItem(links_item)
        link_line = QLineEdit(link)
        treewidget.setItemWidget(link_item, 0, link_line)

def build_list_or_list2(treewidget, parent_item, field):
    field_item = QTreeWidgetItem(parent_item)
    # create widget
    hash_line = QLineEdit(field.hash)
    type_box = QComboBox()
    type_box.addItems(all_bin_types)
    type_box.setCurrentText(field.type.name.lower())
    vtype_box = QComboBox()
    vtype_box.addItems(all_bin_types)
    vtype_box.setCurrentText(field.value_type.name.lower())
    for value in field.data:
        build_value(treewidget, field_item, value, field.value_type, inline=False)
    # set widget
    widget = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(hash_line)
    layout.addWidget(type_box)
    layout.addWidget(vtype_box)
    layout.addStretch()
    widget.setLayout(layout)
    treewidget.setItemWidget(field_item, 0, widget)

def build_pointer_or_embed(treewidget, parent_item, field):
    field_item = QTreeWidgetItem(parent_item)
    # create widget
    hash_line = QLineEdit(field.hash)
    type_box = QComboBox()
    type_box.addItems(all_bin_types)
    type_box.setCurrentText(field.type.name.lower())
    if field.hash_type != '00000000':
        hash_type_line = QLineEdit(field.hash_type)
        for f in field.data:
            build_field(treewidget, field_item, f)
    else:
        hash_type_line = QLineEdit('null')
    # set widget
    widget = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(hash_line, stretch=4)
    layout.addWidget(type_box)
    layout.addWidget(hash_type_line, stretch=6)
    layout.addStretch()
    widget.setLayout(layout)
    treewidget.setItemWidget(field_item, 0, widget)

def build_option(treewidget, parent_item, field):
    field_item = QTreeWidgetItem(parent_item)
    # create widget
    hash_line = QLineEdit(field.hash)
    type_box = QComboBox()
    type_box.addItems(all_bin_types)
    type_box.setCurrentText(field.type.name.lower())
    vtype_box = QComboBox()
    vtype_box.addItems(all_bin_types)
    vtype_box.setCurrentText(field.value_type.name.lower())
    if field.data != None:
        build_value(treewidget, field_item, field.data, field.value_type, inline=False)
    # set widget
    widget = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(hash_line)
    layout.addWidget(type_box)
    layout.addWidget(vtype_box)
    layout.addStretch()
    widget.setLayout(layout)
    treewidget.setItemWidget(field_item, 0, widget)

def build_map(treewidget, parent_item, field):
    field_item = QTreeWidgetItem(parent_item)
    # create widget
    hash_line = QLineEdit(field.hash)
    type_box = QComboBox()
    type_box.addItems(all_bin_types)
    type_box.setCurrentText(field.type.name.lower())
    ktype_box = QComboBox()
    ktype_box.addItems(all_bin_types)
    ktype_box.setCurrentText(field.key_type.name.lower())
    vtype_box = QComboBox()
    vtype_box.addItems(all_bin_types)
    vtype_box.setCurrentText(field.value_type.name.lower())
    for key, value in field.data.items():
        key_item = build_value(treewidget, field_item, key, field.key_type, inline=False)
        build_value(treewidget, key_item, value, field.value_type, inline=False)
    # set widget
    widget = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(hash_line)
    layout.addWidget(type_box)
    layout.addWidget(ktype_box)
    layout.addWidget(vtype_box)
    layout.addStretch()
    widget.setLayout(layout)
    treewidget.setItemWidget(field_item, 0, widget)

def build_value(treewidget, parent_item, value, value_type, inline=True):
    # build value widget
    if value_type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
        value_widget = QTreeWidgetItem(parent_item)
        for v in value.data:
            build_value(treewidget, value_widget, value, value_type, inline=False)
    elif value_type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
        value_item = QTreeWidgetItem(parent_item)
        # create widget
        if value.hash_type != '00000000':
            hash_type_line = QLineEdit(value.hash_type)
            for f in value.data:
                build_field(treewidget, value_item, f)
        else:
            hash_type_line = QLineEdit('null')
        # set widget
        treewidget.setItemWidget(value_item, 0, hash_type_line)
        return value_item
    else:
        value_widget = QLineEdit(str(value))
    # return base on in line
    if inline:
        # inline return the widget so we can add to layout
        return value_widget
    else:
        # not inline mean we build on the child item
        value_item = QTreeWidgetItem(parent_item)
        treewidget.setItemWidget(value_item, 0, value_widget)
        return value_item

def build_field(treewidget: QTreeWidget, parent_item, field):
    if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
        build_list_or_list2(treewidget, parent_item, field)
    elif field.type in (pyRitoFile.bin.BINType.POINTER, pyRitoFile.bin.BINType.EMBED):
        build_pointer_or_embed(treewidget, parent_item, field)
    elif field.type == pyRitoFile.bin.BINType.OPTION:
        build_option(treewidget, parent_item, field)
    elif field.type == pyRitoFile.bin.BINType.MAP:
        build_map(treewidget, parent_item, field)
    else:
        field_item = QTreeWidgetItem(parent_item)
        # create widget
        hash_line = QLineEdit(field.hash)
        type_box = QComboBox()
        type_box.addItems(all_bin_types)
        type_box.setCurrentText(field.type.name.lower())
        value_widget = build_value(treewidget, parent_item, field.data, field.type, inline=True)
        # set widget
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(hash_line, stretch=4)
        layout.addWidget(type_box)
        layout.addWidget(value_widget, stretch=6)
        widget.setLayout(layout)
        treewidget.setItemWidget(field_item, 0, widget)



def build_entries(treewidget: QTreeWidget, entries):
    entries_item = QTreeWidgetItem(treewidget)
    entries_item.setText(0, 'Entries')
    for entry in entries:
        # create widget
        entry_item = QTreeWidgetItem(entries_item)
        hash_line = QLineEdit(entry.hash)
        type_line = QLineEdit(entry.type)
        # set widget
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(hash_line, stretch=6)
        layout.addWidget(type_line, stretch=4)
        widget.setLayout(layout)
        treewidget.setItemWidget(entry_item, 0, widget)
        for field in entry.data:
            build_field(treewidget, entry_item, field)


def create_widget(bin_path):
    # read bin
    hash_helper.Storage.read_all_hashes()
    bin = pyRitoFile.bin.BIN().read(bin_path)
    bin.un_hash(hash_helper.Storage.hashtables)
    hash_helper.Storage.free_all_hashes()
    # create tree widget
    treewidget = QTreeWidget()
    treewidget.setSelectionMode(QTreeWidget.SelectionMode.NoSelection)
    treewidget.setHeaderHidden(True)
    # build tree
    build_links(treewidget, bin.links)
    build_entries(treewidget, bin.entries)
    return treewidget
