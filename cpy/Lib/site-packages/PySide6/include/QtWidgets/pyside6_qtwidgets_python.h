// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTWIDGETS_PYTHON_H
#define SBK_QTWIDGETS_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtgui_python.h>
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QFormLayout>
#include <QTextEdit>
#include <QtGui/qfilesystemmodel.h>
#include <QtWidgets/qabstractitemdelegate.h>
#include <QtWidgets/qabstractitemview.h>
#include <QtWidgets/qabstractscrollarea.h>
#include <QtWidgets/qabstractslider.h>
#include <QtWidgets/qabstractspinbox.h>
#include <QtWidgets/qboxlayout.h>
#include <QtWidgets/qcalendarwidget.h>
#include <QtWidgets/qcolordialog.h>
#include <QtWidgets/qcolormap.h>
#include <QtWidgets/qcombobox.h>
#include <QtWidgets/qcompleter.h>
#include <QtWidgets/qdatawidgetmapper.h>
#include <QtWidgets/qdatetimeedit.h>
#include <QtWidgets/qdialog.h>
#include <QtWidgets/qdialogbuttonbox.h>
#include <QtWidgets/qdockwidget.h>
#include <QtWidgets/qfiledialog.h>
#include <QtWidgets/qfontcombobox.h>
#include <QtWidgets/qfontdialog.h>
#include <QtWidgets/qformlayout.h>
#include <QtWidgets/qframe.h>
#include <QtWidgets/qgesture.h>
#include <QtWidgets/qgesturerecognizer.h>
#include <QtWidgets/qgraphicseffect.h>
#include <QtWidgets/qgraphicsitem.h>
#include <QtWidgets/qgraphicsscene.h>
#include <QtWidgets/qgraphicssceneevent.h>
#include <QtWidgets/qgraphicsview.h>
#include <QtWidgets/qheaderview.h>
#include <QtWidgets/qinputdialog.h>
#include <QtWidgets/qlayout.h>
#include <QtWidgets/qlcdnumber.h>
#include <QtWidgets/qlineedit.h>
#include <QtWidgets/qlistview.h>
#include <QtWidgets/qlistwidget.h>
#include <QtWidgets/qmainwindow.h>
#include <QtWidgets/qmdiarea.h>
#include <QtWidgets/qmdisubwindow.h>
#include <QtWidgets/qmessagebox.h>
#include <QtWidgets/qplaintextedit.h>
#include <QtWidgets/qprogressbar.h>
#include <QtWidgets/qrhiwidget.h>
#include <QtWidgets/qrubberband.h>
#include <QtWidgets/qscroller.h>
#include <QtWidgets/qscrollerproperties.h>
#include <QtWidgets/qsizepolicy.h>
#include <QtWidgets/qslider.h>
#include <QtWidgets/qstackedlayout.h>
#include <QtWidgets/qstyle.h>
#include <QtWidgets/qstyleoption.h>
#include <QtWidgets/qsystemtrayicon.h>
#include <QtWidgets/qtabbar.h>
#include <QtWidgets/qtablewidget.h>
#include <QtWidgets/qtabwidget.h>
#include <QtWidgets/qtextedit.h>
#include <QtWidgets/qtoolbutton.h>
#include <QtWidgets/qtreewidget.h>
#include <QtWidgets/qtreewidgetitemiterator.h>
#include <QtWidgets/qwidget.h>
#include <QtWidgets/qwizard.h>

QT_BEGIN_NAMESPACE
class QAbstractButton;
class QAbstractGraphicsShapeItem;
class QAccessibleWidget;
class QApplication;
class QButtonGroup;
class QCheckBox;
class QColumnView;
class QCommandLinkButton;
class QCommonStyle;
class QDateEdit;
class QDial;
class QDoubleSpinBox;
class QErrorMessage;
class QFileIconProvider;
class QFocusFrame;
class QGestureEvent;
class QGraphicsAnchor;
class QGraphicsAnchorLayout;
class QGraphicsColorizeEffect;
class QGraphicsDropShadowEffect;
class QGraphicsEllipseItem;
class QGraphicsGridLayout;
class QGraphicsItemAnimation;
class QGraphicsItemGroup;
class QGraphicsLayout;
class QGraphicsLayoutItem;
class QGraphicsLineItem;
class QGraphicsLinearLayout;
class QGraphicsObject;
class QGraphicsOpacityEffect;
class QGraphicsPathItem;
class QGraphicsPolygonItem;
class QGraphicsProxyWidget;
class QGraphicsRectItem;
class QGraphicsRotation;
class QGraphicsScale;
class QGraphicsSceneDragDropEvent;
class QGraphicsSceneEvent;
class QGraphicsSceneHelpEvent;
class QGraphicsSceneHoverEvent;
class QGraphicsSceneMouseEvent;
class QGraphicsSceneMoveEvent;
class QGraphicsSceneResizeEvent;
class QGraphicsSceneWheelEvent;
class QGraphicsSimpleTextItem;
class QGraphicsTextItem;
class QGraphicsTransform;
class QGraphicsWidget;
class QGridLayout;
class QGroupBox;
class QHBoxLayout;
class QItemDelegate;
class QItemEditorCreatorBase;
class QItemEditorFactory;
class QKeySequenceEdit;
class QLabel;
class QLayoutItem;
class QListWidget;
class QMenu;
class QMenuBar;
class QPanGesture;
class QPlainTextDocumentLayout;
class QProgressDialog;
class QProxyStyle;
class QPushButton;
class QRadioButton;
class QScrollArea;
class QScrollBar;
class QSizeGrip;
class QSpacerItem;
class QSpinBox;
class QSplashScreen;
class QSplitter;
class QSplitterHandle;
class QStackedWidget;
class QStatusBar;
class QStyleFactory;
class QStylePainter;
class QStyledItemDelegate;
class QTableView;
class QTableWidget;
class QTableWidgetSelectionRange;
class QTapAndHoldGesture;
class QTapGesture;
class QTextBrowser;
struct QTileRules;
class QTimeEdit;
class QToolBar;
class QToolBox;
class QToolTip;
class QTreeView;
class QTreeWidget;
class QUndoView;
class QVBoxLayout;
class QWhatsThis;
class QWidgetAction;
class QWidgetItem;
class QWizardPage;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QABSTRACTBUTTON_IDX                                  = 0,
    SBK_QABSTRACTGRAPHICSSHAPEITEM_IDX                       = 2,
    SBK_QABSTRACTITEMDELEGATE_ENDEDITHINT_IDX                = 6,
    SBK_QABSTRACTITEMDELEGATE_IDX                            = 4,
    SBK_QABSTRACTITEMVIEW_SELECTIONMODE_IDX                  = 24,
    SBK_QABSTRACTITEMVIEW_SELECTIONBEHAVIOR_IDX              = 22,
    SBK_QABSTRACTITEMVIEW_SCROLLHINT_IDX                     = 18,
    SBK_QABSTRACTITEMVIEW_EDITTRIGGER_IDX                    = 16,
    SBK_QFLAGS_QABSTRACTITEMVIEW_EDITTRIGGER_IDX             = 146,
    SBK_QABSTRACTITEMVIEW_SCROLLMODE_IDX                     = 20,
    SBK_QABSTRACTITEMVIEW_DRAGDROPMODE_IDX                   = 12,
    SBK_QABSTRACTITEMVIEW_CURSORACTION_IDX                   = 10,
    SBK_QABSTRACTITEMVIEW_STATE_IDX                          = 26,
    SBK_QABSTRACTITEMVIEW_DROPINDICATORPOSITION_IDX          = 14,
    SBK_QABSTRACTITEMVIEW_IDX                                = 8,
    SBK_QABSTRACTSCROLLAREA_SIZEADJUSTPOLICY_IDX             = 30,
    SBK_QABSTRACTSCROLLAREA_IDX                              = 28,
    SBK_QABSTRACTSLIDER_SLIDERACTION_IDX                     = 34,
    SBK_QABSTRACTSLIDER_SLIDERCHANGE_IDX                     = 36,
    SBK_QABSTRACTSLIDER_IDX                                  = 32,
    SBK_QABSTRACTSPINBOX_STEPENABLEDFLAG_IDX                 = 44,
    SBK_QFLAGS_QABSTRACTSPINBOX_STEPENABLEDFLAG_IDX          = 148,
    SBK_QABSTRACTSPINBOX_BUTTONSYMBOLS_IDX                   = 40,
    SBK_QABSTRACTSPINBOX_CORRECTIONMODE_IDX                  = 42,
    SBK_QABSTRACTSPINBOX_STEPTYPE_IDX                        = 46,
    SBK_QABSTRACTSPINBOX_IDX                                 = 38,
    SBK_QACCESSIBLEWIDGET_IDX                                = 48,
    SBK_QAPPLICATION_IDX                                     = 50,
    SBK_QBOXLAYOUT_DIRECTION_IDX                             = 54,
    SBK_QBOXLAYOUT_IDX                                       = 52,
    SBK_QBUTTONGROUP_IDX                                     = 56,
    SBK_QCALENDARWIDGET_HORIZONTALHEADERFORMAT_IDX           = 60,
    SBK_QCALENDARWIDGET_VERTICALHEADERFORMAT_IDX             = 64,
    SBK_QCALENDARWIDGET_SELECTIONMODE_IDX                    = 62,
    SBK_QCALENDARWIDGET_IDX                                  = 58,
    SBK_QCHECKBOX_IDX                                        = 66,
    SBK_QCOLORDIALOG_COLORDIALOGOPTION_IDX                   = 70,
    SBK_QFLAGS_QCOLORDIALOG_COLORDIALOGOPTION_IDX            = 150,
    SBK_QCOLORDIALOG_IDX                                     = 68,
    SBK_QCOLORMAP_MODE_IDX                                   = 74,
    SBK_QCOLORMAP_IDX                                        = 72,
    SBK_QCOLUMNVIEW_IDX                                      = 76,
    SBK_QCOMBOBOX_INSERTPOLICY_IDX                           = 80,
    SBK_QCOMBOBOX_SIZEADJUSTPOLICY_IDX                       = 82,
    SBK_QCOMBOBOX_IDX                                        = 78,
    SBK_QCOMMANDLINKBUTTON_IDX                               = 84,
    SBK_QCOMMONSTYLE_IDX                                     = 86,
    SBK_QCOMPLETER_COMPLETIONMODE_IDX                        = 90,
    SBK_QCOMPLETER_MODELSORTING_IDX                          = 92,
    SBK_QCOMPLETER_IDX                                       = 88,
    SBK_QDATAWIDGETMAPPER_SUBMITPOLICY_IDX                   = 96,
    SBK_QDATAWIDGETMAPPER_IDX                                = 94,
    SBK_QDATEEDIT_IDX                                        = 98,
    SBK_QDATETIMEEDIT_SECTION_IDX                            = 102,
    SBK_QFLAGS_QDATETIMEEDIT_SECTION_IDX                     = 152,
    SBK_QDATETIMEEDIT_IDX                                    = 100,
    SBK_QDIAL_IDX                                            = 104,
    SBK_QDIALOG_DIALOGCODE_IDX                               = 108,
    SBK_QDIALOG_IDX                                          = 106,
    SBK_QDIALOGBUTTONBOX_BUTTONROLE_IDX                      = 114,
    SBK_QDIALOGBUTTONBOX_STANDARDBUTTON_IDX                  = 116,
    SBK_QFLAGS_QDIALOGBUTTONBOX_STANDARDBUTTON_IDX           = 154,
    SBK_QDIALOGBUTTONBOX_BUTTONLAYOUT_IDX                    = 112,
    SBK_QDIALOGBUTTONBOX_IDX                                 = 110,
    SBK_QDOCKWIDGET_DOCKWIDGETFEATURE_IDX                    = 120,
    SBK_QFLAGS_QDOCKWIDGET_DOCKWIDGETFEATURE_IDX             = 156,
    SBK_QDOCKWIDGET_IDX                                      = 118,
    SBK_QDOUBLESPINBOX_IDX                                   = 122,
    SBK_QERRORMESSAGE_IDX                                    = 124,
    SBK_QFILEDIALOG_VIEWMODE_IDX                             = 136,
    SBK_QFILEDIALOG_FILEMODE_IDX                             = 132,
    SBK_QFILEDIALOG_ACCEPTMODE_IDX                           = 128,
    SBK_QFILEDIALOG_DIALOGLABEL_IDX                          = 130,
    SBK_QFILEDIALOG_OPTION_IDX                               = 134,
    SBK_QFLAGS_QFILEDIALOG_OPTION_IDX                        = 158,
    SBK_QFILEDIALOG_IDX                                      = 126,
    SBK_QFILEICONPROVIDER_IDX                                = 138,
    SBK_QFILESYSTEMMODEL_ROLES_IDX                           = 144,
    SBK_QFILESYSTEMMODEL_OPTION_IDX                          = 142,
    SBK_QFLAGS_QFILESYSTEMMODEL_OPTION_IDX                   = 160,
    SBK_QFILESYSTEMMODEL_IDX                                 = 140,
    SBK_QFOCUSFRAME_IDX                                      = 220,
    SBK_QFONTCOMBOBOX_FONTFILTER_IDX                         = 224,
    SBK_QFLAGS_QFONTCOMBOBOX_FONTFILTER_IDX                  = 162,
    SBK_QFONTCOMBOBOX_IDX                                    = 222,
    SBK_QFONTDIALOG_FONTDIALOGOPTION_IDX                     = 228,
    SBK_QFLAGS_QFONTDIALOG_FONTDIALOGOPTION_IDX              = 164,
    SBK_QFONTDIALOG_IDX                                      = 226,
    SBK_QFORMLAYOUT_FIELDGROWTHPOLICY_IDX                    = 232,
    SBK_QFORMLAYOUT_ROWWRAPPOLICY_IDX                        = 236,
    SBK_QFORMLAYOUT_ITEMROLE_IDX                             = 234,
    SBK_QFORMLAYOUT_IDX                                      = 230,
    SBK_QFORMLAYOUT_TAKEROWRESULT_IDX                        = 238,
    SBK_QFRAME_SHAPE_IDX                                     = 244,
    SBK_QFRAME_SHADOW_IDX                                    = 242,
    SBK_QFRAME_STYLEMASK_IDX                                 = 246,
    SBK_QFRAME_IDX                                           = 240,
    SBK_QGESTURE_GESTURECANCELPOLICY_IDX                     = 250,
    SBK_QGESTURE_IDX                                         = 248,
    SBK_QGESTUREEVENT_IDX                                    = 252,
    SBK_QGESTURERECOGNIZER_RESULTFLAG_IDX                    = 256,
    SBK_QFLAGS_QGESTURERECOGNIZER_RESULTFLAG_IDX             = 166,
    SBK_QGESTURERECOGNIZER_IDX                               = 254,
    SBK_QGRAPHICSANCHOR_IDX                                  = 258,
    SBK_QGRAPHICSANCHORLAYOUT_IDX                            = 260,
    SBK_QGRAPHICSBLUREFFECT_BLURHINT_IDX                     = 264,
    SBK_QFLAGS_QGRAPHICSBLUREFFECT_BLURHINT_IDX              = 168,
    SBK_QGRAPHICSBLUREFFECT_IDX                              = 262,
    SBK_QGRAPHICSCOLORIZEEFFECT_IDX                          = 266,
    SBK_QGRAPHICSDROPSHADOWEFFECT_IDX                        = 268,
    SBK_QGRAPHICSEFFECT_CHANGEFLAG_IDX                       = 272,
    SBK_QFLAGS_QGRAPHICSEFFECT_CHANGEFLAG_IDX                = 170,
    SBK_QGRAPHICSEFFECT_PIXMAPPADMODE_IDX                    = 274,
    SBK_QGRAPHICSEFFECT_IDX                                  = 270,
    SBK_QGRAPHICSELLIPSEITEM_IDX                             = 276,
    SBK_QGRAPHICSGRIDLAYOUT_IDX                              = 278,
    SBK_QGRAPHICSITEM_GRAPHICSITEMFLAG_IDX                   = 288,
    SBK_QFLAGS_QGRAPHICSITEM_GRAPHICSITEMFLAG_IDX            = 172,
    SBK_QGRAPHICSITEM_GRAPHICSITEMCHANGE_IDX                 = 286,
    SBK_QGRAPHICSITEM_CACHEMODE_IDX                          = 282,
    SBK_QGRAPHICSITEM_PANELMODALITY_IDX                      = 290,
    SBK_QGRAPHICSITEM_EXTENSION_IDX                          = 284,
    SBK_QGRAPHICSITEM_IDX                                    = 280,
    SBK_QGRAPHICSITEMANIMATION_IDX                           = 292,
    SBK_QGRAPHICSITEMGROUP_IDX                               = 294,
    SBK_QGRAPHICSLAYOUT_IDX                                  = 296,
    SBK_QGRAPHICSLAYOUTITEM_IDX                              = 298,
    SBK_QGRAPHICSLINEITEM_IDX                                = 300,
    SBK_QGRAPHICSLINEARLAYOUT_IDX                            = 302,
    SBK_QGRAPHICSOBJECT_IDX                                  = 304,
    SBK_QGRAPHICSOPACITYEFFECT_IDX                           = 306,
    SBK_QGRAPHICSPATHITEM_IDX                                = 308,
    SBK_QGRAPHICSPIXMAPITEM_SHAPEMODE_IDX                    = 312,
    SBK_QGRAPHICSPIXMAPITEM_IDX                              = 310,
    SBK_QGRAPHICSPOLYGONITEM_IDX                             = 314,
    SBK_QGRAPHICSPROXYWIDGET_IDX                             = 316,
    SBK_QGRAPHICSRECTITEM_IDX                                = 318,
    SBK_QGRAPHICSROTATION_IDX                                = 320,
    SBK_QGRAPHICSSCALE_IDX                                   = 322,
    SBK_QGRAPHICSSCENE_ITEMINDEXMETHOD_IDX                   = 326,
    SBK_QGRAPHICSSCENE_SCENELAYER_IDX                        = 328,
    SBK_QFLAGS_QGRAPHICSSCENE_SCENELAYER_IDX                 = 174,
    SBK_QGRAPHICSSCENE_IDX                                   = 324,
    SBK_QGRAPHICSSCENECONTEXTMENUEVENT_REASON_IDX            = 332,
    SBK_QGRAPHICSSCENECONTEXTMENUEVENT_IDX                   = 330,
    SBK_QGRAPHICSSCENEDRAGDROPEVENT_IDX                      = 334,
    SBK_QGRAPHICSSCENEEVENT_IDX                              = 336,
    SBK_QGRAPHICSSCENEHELPEVENT_IDX                          = 338,
    SBK_QGRAPHICSSCENEHOVEREVENT_IDX                         = 340,
    SBK_QGRAPHICSSCENEMOUSEEVENT_IDX                         = 342,
    SBK_QGRAPHICSSCENEMOVEEVENT_IDX                          = 344,
    SBK_QGRAPHICSSCENERESIZEEVENT_IDX                        = 346,
    SBK_QGRAPHICSSCENEWHEELEVENT_IDX                         = 348,
    SBK_QGRAPHICSSIMPLETEXTITEM_IDX                          = 350,
    SBK_QGRAPHICSTEXTITEM_IDX                                = 352,
    SBK_QGRAPHICSTRANSFORM_IDX                               = 354,
    SBK_QGRAPHICSVIEW_VIEWPORTANCHOR_IDX                     = 364,
    SBK_QGRAPHICSVIEW_CACHEMODEFLAG_IDX                      = 358,
    SBK_QFLAGS_QGRAPHICSVIEW_CACHEMODEFLAG_IDX               = 176,
    SBK_QGRAPHICSVIEW_DRAGMODE_IDX                           = 360,
    SBK_QGRAPHICSVIEW_VIEWPORTUPDATEMODE_IDX                 = 366,
    SBK_QGRAPHICSVIEW_OPTIMIZATIONFLAG_IDX                   = 362,
    SBK_QFLAGS_QGRAPHICSVIEW_OPTIMIZATIONFLAG_IDX            = 178,
    SBK_QGRAPHICSVIEW_IDX                                    = 356,
    SBK_QGRAPHICSWIDGET_IDX                                  = 368,
    SBK_QGRIDLAYOUT_IDX                                      = 370,
    SBK_QGROUPBOX_IDX                                        = 372,
    SBK_QHBOXLAYOUT_IDX                                      = 374,
    SBK_QHEADERVIEW_RESIZEMODE_IDX                           = 378,
    SBK_QHEADERVIEW_IDX                                      = 376,
    SBK_QINPUTDIALOG_INPUTDIALOGOPTION_IDX                   = 382,
    SBK_QINPUTDIALOG_INPUTMODE_IDX                           = 384,
    SBK_QINPUTDIALOG_IDX                                     = 380,
    SBK_QITEMDELEGATE_IDX                                    = 386,
    SBK_QITEMEDITORCREATORBASE_IDX                           = 388,
    SBK_QITEMEDITORFACTORY_IDX                               = 390,
    SBK_QKEYSEQUENCEEDIT_IDX                                 = 392,
    SBK_QLCDNUMBER_MODE_IDX                                  = 396,
    SBK_QLCDNUMBER_SEGMENTSTYLE_IDX                          = 398,
    SBK_QLCDNUMBER_IDX                                       = 394,
    SBK_QLABEL_IDX                                           = 400,
    SBK_QLAYOUT_SIZECONSTRAINT_IDX                           = 404,
    SBK_QLAYOUT_IDX                                          = 402,
    SBK_QLAYOUTITEM_IDX                                      = 406,
    SBK_QLINEEDIT_ACTIONPOSITION_IDX                         = 410,
    SBK_QLINEEDIT_ECHOMODE_IDX                               = 412,
    SBK_QLINEEDIT_IDX                                        = 408,
    SBK_QLISTVIEW_MOVEMENT_IDX                               = 420,
    SBK_QLISTVIEW_FLOW_IDX                                   = 416,
    SBK_QLISTVIEW_RESIZEMODE_IDX                             = 422,
    SBK_QLISTVIEW_LAYOUTMODE_IDX                             = 418,
    SBK_QLISTVIEW_VIEWMODE_IDX                               = 424,
    SBK_QLISTVIEW_IDX                                        = 414,
    SBK_QLISTWIDGET_IDX                                      = 426,
    SBK_QLISTWIDGETITEM_ITEMTYPE_IDX                         = 430,
    SBK_QLISTWIDGETITEM_IDX                                  = 428,
    SBK_QMAINWINDOW_DOCKOPTION_IDX                           = 434,
    SBK_QFLAGS_QMAINWINDOW_DOCKOPTION_IDX                    = 180,
    SBK_QMAINWINDOW_IDX                                      = 432,
    SBK_QMDIAREA_AREAOPTION_IDX                              = 438,
    SBK_QFLAGS_QMDIAREA_AREAOPTION_IDX                       = 182,
    SBK_QMDIAREA_WINDOWORDER_IDX                             = 442,
    SBK_QMDIAREA_VIEWMODE_IDX                                = 440,
    SBK_QMDIAREA_IDX                                         = 436,
    SBK_QMDISUBWINDOW_SUBWINDOWOPTION_IDX                    = 446,
    SBK_QFLAGS_QMDISUBWINDOW_SUBWINDOWOPTION_IDX             = 184,
    SBK_QMDISUBWINDOW_IDX                                    = 444,
    SBK_QMENU_IDX                                            = 448,
    SBK_QMENUBAR_IDX                                         = 450,
    SBK_QMESSAGEBOX_OPTION_IDX                               = 458,
    SBK_QFLAGS_QMESSAGEBOX_OPTION_IDX                        = 186,
    SBK_QMESSAGEBOX_ICON_IDX                                 = 456,
    SBK_QMESSAGEBOX_BUTTONROLE_IDX                           = 454,
    SBK_QMESSAGEBOX_STANDARDBUTTON_IDX                       = 460,
    SBK_QFLAGS_QMESSAGEBOX_STANDARDBUTTON_IDX                = 188,
    SBK_QMESSAGEBOX_IDX                                      = 452,
    SBK_QPANGESTURE_IDX                                      = 462,
    SBK_QPINCHGESTURE_CHANGEFLAG_IDX                         = 466,
    SBK_QFLAGS_QPINCHGESTURE_CHANGEFLAG_IDX                  = 190,
    SBK_QPINCHGESTURE_IDX                                    = 464,
    SBK_QPLAINTEXTDOCUMENTLAYOUT_IDX                         = 468,
    SBK_QPLAINTEXTEDIT_LINEWRAPMODE_IDX                      = 472,
    SBK_QPLAINTEXTEDIT_IDX                                   = 470,
    SBK_QPROGRESSBAR_DIRECTION_IDX                           = 476,
    SBK_QPROGRESSBAR_IDX                                     = 474,
    SBK_QPROGRESSDIALOG_IDX                                  = 478,
    SBK_QPROXYSTYLE_IDX                                      = 480,
    SBK_QPUSHBUTTON_IDX                                      = 482,
    SBK_QRADIOBUTTON_IDX                                     = 484,
    SBK_QRHIWIDGET_API_IDX                                   = 488,
    SBK_QRHIWIDGET_TEXTUREFORMAT_IDX                         = 490,
    SBK_QRHIWIDGET_IDX                                       = 486,
    SBK_QRUBBERBAND_SHAPE_IDX                                = 494,
    SBK_QRUBBERBAND_IDX                                      = 492,
    SBK_QSCROLLAREA_IDX                                      = 496,
    SBK_QSCROLLBAR_IDX                                       = 498,
    SBK_QSCROLLER_STATE_IDX                                  = 506,
    SBK_QSCROLLER_SCROLLERGESTURETYPE_IDX                    = 504,
    SBK_QSCROLLER_INPUT_IDX                                  = 502,
    SBK_QSCROLLER_IDX                                        = 500,
    SBK_QSCROLLERPROPERTIES_OVERSHOOTPOLICY_IDX              = 512,
    SBK_QSCROLLERPROPERTIES_FRAMERATES_IDX                   = 510,
    SBK_QSCROLLERPROPERTIES_SCROLLMETRIC_IDX                 = 514,
    SBK_QSCROLLERPROPERTIES_IDX                              = 508,
    SBK_QSIZEGRIP_IDX                                        = 516,
    SBK_QSIZEPOLICY_POLICYFLAG_IDX                           = 524,
    SBK_QSIZEPOLICY_POLICY_IDX                               = 522,
    SBK_QSIZEPOLICY_CONTROLTYPE_IDX                          = 520,
    SBK_QFLAGS_QSIZEPOLICY_CONTROLTYPE_IDX                   = 192,
    SBK_QSIZEPOLICY_IDX                                      = 518,
    SBK_QSLIDER_TICKPOSITION_IDX                             = 528,
    SBK_QSLIDER_IDX                                          = 526,
    SBK_QSPACERITEM_IDX                                      = 530,
    SBK_QSPINBOX_IDX                                         = 532,
    SBK_QSPLASHSCREEN_IDX                                    = 534,
    SBK_QSPLITTER_IDX                                        = 536,
    SBK_QSPLITTERHANDLE_IDX                                  = 538,
    SBK_QSTACKEDLAYOUT_STACKINGMODE_IDX                      = 542,
    SBK_QSTACKEDLAYOUT_IDX                                   = 540,
    SBK_QSTACKEDWIDGET_IDX                                   = 544,
    SBK_QSTATUSBAR_IDX                                       = 546,
    SBK_QSTYLE_STATEFLAG_IDX                                 = 564,
    SBK_QFLAGS_QSTYLE_STATEFLAG_IDX                          = 194,
    SBK_QSTYLE_PRIMITIVEELEMENT_IDX                          = 558,
    SBK_QSTYLE_CONTROLELEMENT_IDX                            = 554,
    SBK_QSTYLE_SUBELEMENT_IDX                                = 570,
    SBK_QSTYLE_COMPLEXCONTROL_IDX                            = 550,
    SBK_QSTYLE_SUBCONTROL_IDX                                = 568,
    SBK_QFLAGS_QSTYLE_SUBCONTROL_IDX                         = 196,
    SBK_QSTYLE_PIXELMETRIC_IDX                               = 556,
    SBK_QSTYLE_CONTENTSTYPE_IDX                              = 552,
    SBK_QSTYLE_REQUESTSOFTWAREINPUTPANEL_IDX                 = 560,
    SBK_QSTYLE_STYLEHINT_IDX                                 = 566,
    SBK_QSTYLE_STANDARDPIXMAP_IDX                            = 562,
    SBK_QSTYLE_IDX                                           = 548,
    SBK_QSTYLEFACTORY_IDX                                    = 572,
    SBK_QSTYLEHINTRETURN_HINTRETURNTYPE_IDX                  = 576,
    SBK_QSTYLEHINTRETURN_STYLEOPTIONTYPE_IDX                 = 578,
    SBK_QSTYLEHINTRETURN_STYLEOPTIONVERSION_IDX              = 580,
    SBK_QSTYLEHINTRETURN_IDX                                 = 574,
    SBK_QSTYLEHINTRETURNMASK_STYLEOPTIONTYPE_IDX             = 584,
    SBK_QSTYLEHINTRETURNMASK_STYLEOPTIONVERSION_IDX          = 586,
    SBK_QSTYLEHINTRETURNMASK_IDX                             = 582,
    SBK_QSTYLEHINTRETURNVARIANT_STYLEOPTIONTYPE_IDX          = 590,
    SBK_QSTYLEHINTRETURNVARIANT_STYLEOPTIONVERSION_IDX       = 592,
    SBK_QSTYLEHINTRETURNVARIANT_IDX                          = 588,
    SBK_QSTYLEOPTION_OPTIONTYPE_IDX                          = 596,
    SBK_QSTYLEOPTION_STYLEOPTIONTYPE_IDX                     = 598,
    SBK_QSTYLEOPTION_STYLEOPTIONVERSION_IDX                  = 600,
    SBK_QSTYLEOPTION_IDX                                     = 594,
    SBK_QSTYLEOPTIONBUTTON_STYLEOPTIONTYPE_IDX               = 606,
    SBK_QSTYLEOPTIONBUTTON_STYLEOPTIONVERSION_IDX            = 608,
    SBK_QSTYLEOPTIONBUTTON_BUTTONFEATURE_IDX                 = 604,
    SBK_QFLAGS_QSTYLEOPTIONBUTTON_BUTTONFEATURE_IDX          = 198,
    SBK_QSTYLEOPTIONBUTTON_IDX                               = 602,
    SBK_QSTYLEOPTIONCOMBOBOX_STYLEOPTIONTYPE_IDX             = 612,
    SBK_QSTYLEOPTIONCOMBOBOX_STYLEOPTIONVERSION_IDX          = 614,
    SBK_QSTYLEOPTIONCOMBOBOX_IDX                             = 610,
    SBK_QSTYLEOPTIONCOMPLEX_STYLEOPTIONTYPE_IDX              = 618,
    SBK_QSTYLEOPTIONCOMPLEX_STYLEOPTIONVERSION_IDX           = 620,
    SBK_QSTYLEOPTIONCOMPLEX_IDX                              = 616,
    SBK_QSTYLEOPTIONDOCKWIDGET_STYLEOPTIONTYPE_IDX           = 624,
    SBK_QSTYLEOPTIONDOCKWIDGET_STYLEOPTIONVERSION_IDX        = 626,
    SBK_QSTYLEOPTIONDOCKWIDGET_IDX                           = 622,
    SBK_QSTYLEOPTIONFOCUSRECT_STYLEOPTIONTYPE_IDX            = 630,
    SBK_QSTYLEOPTIONFOCUSRECT_STYLEOPTIONVERSION_IDX         = 632,
    SBK_QSTYLEOPTIONFOCUSRECT_IDX                            = 628,
    SBK_QSTYLEOPTIONFRAME_STYLEOPTIONTYPE_IDX                = 638,
    SBK_QSTYLEOPTIONFRAME_STYLEOPTIONVERSION_IDX             = 640,
    SBK_QSTYLEOPTIONFRAME_FRAMEFEATURE_IDX                   = 636,
    SBK_QFLAGS_QSTYLEOPTIONFRAME_FRAMEFEATURE_IDX            = 200,
    SBK_QSTYLEOPTIONFRAME_IDX                                = 634,
    SBK_QSTYLEOPTIONGRAPHICSITEM_STYLEOPTIONTYPE_IDX         = 644,
    SBK_QSTYLEOPTIONGRAPHICSITEM_STYLEOPTIONVERSION_IDX      = 646,
    SBK_QSTYLEOPTIONGRAPHICSITEM_IDX                         = 642,
    SBK_QSTYLEOPTIONGROUPBOX_STYLEOPTIONTYPE_IDX             = 650,
    SBK_QSTYLEOPTIONGROUPBOX_STYLEOPTIONVERSION_IDX          = 652,
    SBK_QSTYLEOPTIONGROUPBOX_IDX                             = 648,
    SBK_QSTYLEOPTIONHEADER_STYLEOPTIONTYPE_IDX               = 662,
    SBK_QSTYLEOPTIONHEADER_STYLEOPTIONVERSION_IDX            = 664,
    SBK_QSTYLEOPTIONHEADER_SECTIONPOSITION_IDX               = 656,
    SBK_QSTYLEOPTIONHEADER_SELECTEDPOSITION_IDX              = 658,
    SBK_QSTYLEOPTIONHEADER_SORTINDICATOR_IDX                 = 660,
    SBK_QSTYLEOPTIONHEADER_IDX                               = 654,
    SBK_QSTYLEOPTIONHEADERV2_STYLEOPTIONTYPE_IDX             = 668,
    SBK_QSTYLEOPTIONHEADERV2_STYLEOPTIONVERSION_IDX          = 670,
    SBK_QSTYLEOPTIONHEADERV2_IDX                             = 666,
    SBK_QSTYLEOPTIONMENUITEM_STYLEOPTIONTYPE_IDX             = 678,
    SBK_QSTYLEOPTIONMENUITEM_STYLEOPTIONVERSION_IDX          = 680,
    SBK_QSTYLEOPTIONMENUITEM_MENUITEMTYPE_IDX                = 676,
    SBK_QSTYLEOPTIONMENUITEM_CHECKTYPE_IDX                   = 674,
    SBK_QSTYLEOPTIONMENUITEM_IDX                             = 672,
    SBK_QSTYLEOPTIONPROGRESSBAR_STYLEOPTIONTYPE_IDX          = 684,
    SBK_QSTYLEOPTIONPROGRESSBAR_STYLEOPTIONVERSION_IDX       = 686,
    SBK_QSTYLEOPTIONPROGRESSBAR_IDX                          = 682,
    SBK_QSTYLEOPTIONRUBBERBAND_STYLEOPTIONTYPE_IDX           = 690,
    SBK_QSTYLEOPTIONRUBBERBAND_STYLEOPTIONVERSION_IDX        = 692,
    SBK_QSTYLEOPTIONRUBBERBAND_IDX                           = 688,
    SBK_QSTYLEOPTIONSIZEGRIP_STYLEOPTIONTYPE_IDX             = 696,
    SBK_QSTYLEOPTIONSIZEGRIP_STYLEOPTIONVERSION_IDX          = 698,
    SBK_QSTYLEOPTIONSIZEGRIP_IDX                             = 694,
    SBK_QSTYLEOPTIONSLIDER_STYLEOPTIONTYPE_IDX               = 702,
    SBK_QSTYLEOPTIONSLIDER_STYLEOPTIONVERSION_IDX            = 704,
    SBK_QSTYLEOPTIONSLIDER_IDX                               = 700,
    SBK_QSTYLEOPTIONSPINBOX_STYLEOPTIONTYPE_IDX              = 708,
    SBK_QSTYLEOPTIONSPINBOX_STYLEOPTIONVERSION_IDX           = 710,
    SBK_QSTYLEOPTIONSPINBOX_IDX                              = 706,
    SBK_QSTYLEOPTIONTAB_STYLEOPTIONTYPE_IDX                  = 718,
    SBK_QSTYLEOPTIONTAB_STYLEOPTIONVERSION_IDX               = 720,
    SBK_QSTYLEOPTIONTAB_TABPOSITION_IDX                      = 724,
    SBK_QSTYLEOPTIONTAB_SELECTEDPOSITION_IDX                 = 716,
    SBK_QSTYLEOPTIONTAB_CORNERWIDGET_IDX                     = 714,
    SBK_QFLAGS_QSTYLEOPTIONTAB_CORNERWIDGET_IDX              = 202,
    SBK_QSTYLEOPTIONTAB_TABFEATURE_IDX                       = 722,
    SBK_QFLAGS_QSTYLEOPTIONTAB_TABFEATURE_IDX                = 204,
    SBK_QSTYLEOPTIONTAB_IDX                                  = 712,
    SBK_QSTYLEOPTIONTABBARBASE_STYLEOPTIONTYPE_IDX           = 728,
    SBK_QSTYLEOPTIONTABBARBASE_STYLEOPTIONVERSION_IDX        = 730,
    SBK_QSTYLEOPTIONTABBARBASE_IDX                           = 726,
    SBK_QSTYLEOPTIONTABWIDGETFRAME_STYLEOPTIONTYPE_IDX       = 734,
    SBK_QSTYLEOPTIONTABWIDGETFRAME_STYLEOPTIONVERSION_IDX    = 736,
    SBK_QSTYLEOPTIONTABWIDGETFRAME_IDX                       = 732,
    SBK_QSTYLEOPTIONTITLEBAR_STYLEOPTIONTYPE_IDX             = 740,
    SBK_QSTYLEOPTIONTITLEBAR_STYLEOPTIONVERSION_IDX          = 742,
    SBK_QSTYLEOPTIONTITLEBAR_IDX                             = 738,
    SBK_QSTYLEOPTIONTOOLBAR_STYLEOPTIONTYPE_IDX              = 746,
    SBK_QSTYLEOPTIONTOOLBAR_STYLEOPTIONVERSION_IDX           = 748,
    SBK_QSTYLEOPTIONTOOLBAR_TOOLBARPOSITION_IDX              = 752,
    SBK_QSTYLEOPTIONTOOLBAR_TOOLBARFEATURE_IDX               = 750,
    SBK_QFLAGS_QSTYLEOPTIONTOOLBAR_TOOLBARFEATURE_IDX        = 206,
    SBK_QSTYLEOPTIONTOOLBAR_IDX                              = 744,
    SBK_QSTYLEOPTIONTOOLBOX_STYLEOPTIONTYPE_IDX              = 758,
    SBK_QSTYLEOPTIONTOOLBOX_STYLEOPTIONVERSION_IDX           = 760,
    SBK_QSTYLEOPTIONTOOLBOX_TABPOSITION_IDX                  = 762,
    SBK_QSTYLEOPTIONTOOLBOX_SELECTEDPOSITION_IDX             = 756,
    SBK_QSTYLEOPTIONTOOLBOX_IDX                              = 754,
    SBK_QSTYLEOPTIONTOOLBUTTON_STYLEOPTIONTYPE_IDX           = 766,
    SBK_QSTYLEOPTIONTOOLBUTTON_STYLEOPTIONVERSION_IDX        = 768,
    SBK_QSTYLEOPTIONTOOLBUTTON_TOOLBUTTONFEATURE_IDX         = 770,
    SBK_QFLAGS_QSTYLEOPTIONTOOLBUTTON_TOOLBUTTONFEATURE_IDX  = 208,
    SBK_QSTYLEOPTIONTOOLBUTTON_IDX                           = 764,
    SBK_QSTYLEOPTIONVIEWITEM_STYLEOPTIONTYPE_IDX             = 776,
    SBK_QSTYLEOPTIONVIEWITEM_STYLEOPTIONVERSION_IDX          = 778,
    SBK_QSTYLEOPTIONVIEWITEM_POSITION_IDX                    = 774,
    SBK_QSTYLEOPTIONVIEWITEM_VIEWITEMFEATURE_IDX             = 780,
    SBK_QFLAGS_QSTYLEOPTIONVIEWITEM_VIEWITEMFEATURE_IDX      = 210,
    SBK_QSTYLEOPTIONVIEWITEM_VIEWITEMPOSITION_IDX            = 782,
    SBK_QSTYLEOPTIONVIEWITEM_IDX                             = 772,
    SBK_QSTYLEPAINTER_IDX                                    = 784,
    SBK_QSTYLEDITEMDELEGATE_IDX                              = 786,
    SBK_QSWIPEGESTURE_SWIPEDIRECTION_IDX                     = 790,
    SBK_QSWIPEGESTURE_IDX                                    = 788,
    SBK_QSYSTEMTRAYICON_ACTIVATIONREASON_IDX                 = 794,
    SBK_QSYSTEMTRAYICON_MESSAGEICON_IDX                      = 796,
    SBK_QSYSTEMTRAYICON_IDX                                  = 792,
    SBK_QTABBAR_SHAPE_IDX                                    = 804,
    SBK_QTABBAR_BUTTONPOSITION_IDX                           = 800,
    SBK_QTABBAR_SELECTIONBEHAVIOR_IDX                        = 802,
    SBK_QTABBAR_IDX                                          = 798,
    SBK_QTABWIDGET_TABPOSITION_IDX                           = 808,
    SBK_QTABWIDGET_TABSHAPE_IDX                              = 810,
    SBK_QTABWIDGET_IDX                                       = 806,
    SBK_QTABLEVIEW_IDX                                       = 812,
    SBK_QTABLEWIDGET_IDX                                     = 814,
    SBK_QTABLEWIDGETITEM_ITEMTYPE_IDX                        = 818,
    SBK_QTABLEWIDGETITEM_IDX                                 = 816,
    SBK_QTABLEWIDGETSELECTIONRANGE_IDX                       = 820,
    SBK_QTAPANDHOLDGESTURE_IDX                               = 822,
    SBK_QTAPGESTURE_IDX                                      = 824,
    SBK_QTEXTBROWSER_IDX                                     = 826,
    SBK_QTEXTEDIT_LINEWRAPMODE_IDX                           = 834,
    SBK_QTEXTEDIT_AUTOFORMATTINGFLAG_IDX                     = 830,
    SBK_QFLAGS_QTEXTEDIT_AUTOFORMATTINGFLAG_IDX              = 212,
    SBK_QTEXTEDIT_IDX                                        = 828,
    SBK_QTEXTEDIT_EXTRASELECTION_IDX                         = 832,
    SBK_QTILERULES_IDX                                       = 836,
    SBK_QTIMEEDIT_IDX                                        = 838,
    SBK_QTOOLBAR_IDX                                         = 840,
    SBK_QTOOLBOX_IDX                                         = 842,
    SBK_QTOOLBUTTON_TOOLBUTTONPOPUPMODE_IDX                  = 846,
    SBK_QTOOLBUTTON_IDX                                      = 844,
    SBK_QTOOLTIP_IDX                                         = 848,
    SBK_QTREEVIEW_IDX                                        = 850,
    SBK_QTREEWIDGET_IDX                                      = 852,
    SBK_QTREEWIDGETITEM_ITEMTYPE_IDX                         = 858,
    SBK_QTREEWIDGETITEM_CHILDINDICATORPOLICY_IDX             = 856,
    SBK_QTREEWIDGETITEM_IDX                                  = 854,
    SBK_QTREEWIDGETITEMITERATOR_ITERATORFLAG_IDX             = 862,
    SBK_QFLAGS_QTREEWIDGETITEMITERATOR_ITERATORFLAG_IDX      = 214,
    SBK_QTREEWIDGETITEMITERATOR_IDX                          = 860,
    SBK_QUNDOVIEW_IDX                                        = 864,
    SBK_QVBOXLAYOUT_IDX                                      = 866,
    SBK_QWHATSTHIS_IDX                                       = 868,
    SBK_QWIDGET_RENDERFLAG_IDX                               = 872,
    SBK_QFLAGS_QWIDGET_RENDERFLAG_IDX                        = 216,
    SBK_QWIDGET_IDX                                          = 870,
    SBK_QWIDGETACTION_IDX                                    = 874,
    SBK_QWIDGETITEM_IDX                                      = 876,
    SBK_QWIZARD_WIZARDBUTTON_IDX                             = 880,
    SBK_QWIZARD_WIZARDPIXMAP_IDX                             = 884,
    SBK_QWIZARD_WIZARDSTYLE_IDX                              = 886,
    SBK_QWIZARD_WIZARDOPTION_IDX                             = 882,
    SBK_QFLAGS_QWIZARD_WIZARDOPTION_IDX                      = 218,
    SBK_QWIZARD_IDX                                          = 878,
    SBK_QWIZARDPAGE_IDX                                      = 888,
    SBK_QTWIDGETS_IDX_COUNT                                  = 890,
};

// Type indices
enum : int {
    SBK_QAbstractButton_IDX                                  = 0,
    SBK_QAbstractGraphicsShapeItem_IDX                       = 1,
    SBK_QAbstractItemDelegate_EndEditHint_IDX                = 3,
    SBK_QAbstractItemDelegate_IDX                            = 2,
    SBK_QAbstractItemView_SelectionMode_IDX                  = 12,
    SBK_QAbstractItemView_SelectionBehavior_IDX              = 11,
    SBK_QAbstractItemView_ScrollHint_IDX                     = 9,
    SBK_QAbstractItemView_EditTrigger_IDX                    = 8,
    SBK_QFlags_QAbstractItemView_EditTrigger_IDX             = 73,
    SBK_QAbstractItemView_ScrollMode_IDX                     = 10,
    SBK_QAbstractItemView_DragDropMode_IDX                   = 6,
    SBK_QAbstractItemView_CursorAction_IDX                   = 5,
    SBK_QAbstractItemView_State_IDX                          = 13,
    SBK_QAbstractItemView_DropIndicatorPosition_IDX          = 7,
    SBK_QAbstractItemView_IDX                                = 4,
    SBK_QAbstractScrollArea_SizeAdjustPolicy_IDX             = 15,
    SBK_QAbstractScrollArea_IDX                              = 14,
    SBK_QAbstractSlider_SliderAction_IDX                     = 17,
    SBK_QAbstractSlider_SliderChange_IDX                     = 18,
    SBK_QAbstractSlider_IDX                                  = 16,
    SBK_QAbstractSpinBox_StepEnabledFlag_IDX                 = 22,
    SBK_QFlags_QAbstractSpinBox_StepEnabledFlag_IDX          = 74,
    SBK_QAbstractSpinBox_ButtonSymbols_IDX                   = 20,
    SBK_QAbstractSpinBox_CorrectionMode_IDX                  = 21,
    SBK_QAbstractSpinBox_StepType_IDX                        = 23,
    SBK_QAbstractSpinBox_IDX                                 = 19,
    SBK_QAccessibleWidget_IDX                                = 24,
    SBK_QApplication_IDX                                     = 25,
    SBK_QBoxLayout_Direction_IDX                             = 27,
    SBK_QBoxLayout_IDX                                       = 26,
    SBK_QButtonGroup_IDX                                     = 28,
    SBK_QCalendarWidget_HorizontalHeaderFormat_IDX           = 30,
    SBK_QCalendarWidget_VerticalHeaderFormat_IDX             = 32,
    SBK_QCalendarWidget_SelectionMode_IDX                    = 31,
    SBK_QCalendarWidget_IDX                                  = 29,
    SBK_QCheckBox_IDX                                        = 33,
    SBK_QColorDialog_ColorDialogOption_IDX                   = 35,
    SBK_QFlags_QColorDialog_ColorDialogOption_IDX            = 75,
    SBK_QColorDialog_IDX                                     = 34,
    SBK_QColormap_Mode_IDX                                   = 37,
    SBK_QColormap_IDX                                        = 36,
    SBK_QColumnView_IDX                                      = 38,
    SBK_QComboBox_InsertPolicy_IDX                           = 40,
    SBK_QComboBox_SizeAdjustPolicy_IDX                       = 41,
    SBK_QComboBox_IDX                                        = 39,
    SBK_QCommandLinkButton_IDX                               = 42,
    SBK_QCommonStyle_IDX                                     = 43,
    SBK_QCompleter_CompletionMode_IDX                        = 45,
    SBK_QCompleter_ModelSorting_IDX                          = 46,
    SBK_QCompleter_IDX                                       = 44,
    SBK_QDataWidgetMapper_SubmitPolicy_IDX                   = 48,
    SBK_QDataWidgetMapper_IDX                                = 47,
    SBK_QDateEdit_IDX                                        = 49,
    SBK_QDateTimeEdit_Section_IDX                            = 51,
    SBK_QFlags_QDateTimeEdit_Section_IDX                     = 76,
    SBK_QDateTimeEdit_IDX                                    = 50,
    SBK_QDial_IDX                                            = 52,
    SBK_QDialog_DialogCode_IDX                               = 54,
    SBK_QDialog_IDX                                          = 53,
    SBK_QDialogButtonBox_ButtonRole_IDX                      = 57,
    SBK_QDialogButtonBox_StandardButton_IDX                  = 58,
    SBK_QFlags_QDialogButtonBox_StandardButton_IDX           = 77,
    SBK_QDialogButtonBox_ButtonLayout_IDX                    = 56,
    SBK_QDialogButtonBox_IDX                                 = 55,
    SBK_QDockWidget_DockWidgetFeature_IDX                    = 60,
    SBK_QFlags_QDockWidget_DockWidgetFeature_IDX             = 78,
    SBK_QDockWidget_IDX                                      = 59,
    SBK_QDoubleSpinBox_IDX                                   = 61,
    SBK_QErrorMessage_IDX                                    = 62,
    SBK_QFileDialog_ViewMode_IDX                             = 68,
    SBK_QFileDialog_FileMode_IDX                             = 66,
    SBK_QFileDialog_AcceptMode_IDX                           = 64,
    SBK_QFileDialog_DialogLabel_IDX                          = 65,
    SBK_QFileDialog_Option_IDX                               = 67,
    SBK_QFlags_QFileDialog_Option_IDX                        = 79,
    SBK_QFileDialog_IDX                                      = 63,
    SBK_QFileIconProvider_IDX                                = 69,
    SBK_QFileSystemModel_Roles_IDX                           = 72,
    SBK_QFileSystemModel_Option_IDX                          = 71,
    SBK_QFlags_QFileSystemModel_Option_IDX                   = 80,
    SBK_QFileSystemModel_IDX                                 = 70,
    SBK_QFocusFrame_IDX                                      = 110,
    SBK_QFontComboBox_FontFilter_IDX                         = 112,
    SBK_QFlags_QFontComboBox_FontFilter_IDX                  = 81,
    SBK_QFontComboBox_IDX                                    = 111,
    SBK_QFontDialog_FontDialogOption_IDX                     = 114,
    SBK_QFlags_QFontDialog_FontDialogOption_IDX              = 82,
    SBK_QFontDialog_IDX                                      = 113,
    SBK_QFormLayout_FieldGrowthPolicy_IDX                    = 116,
    SBK_QFormLayout_RowWrapPolicy_IDX                        = 118,
    SBK_QFormLayout_ItemRole_IDX                             = 117,
    SBK_QFormLayout_IDX                                      = 115,
    SBK_QFormLayout_TakeRowResult_IDX                        = 119,
    SBK_QFrame_Shape_IDX                                     = 122,
    SBK_QFrame_Shadow_IDX                                    = 121,
    SBK_QFrame_StyleMask_IDX                                 = 123,
    SBK_QFrame_IDX                                           = 120,
    SBK_QGesture_GestureCancelPolicy_IDX                     = 125,
    SBK_QGesture_IDX                                         = 124,
    SBK_QGestureEvent_IDX                                    = 126,
    SBK_QGestureRecognizer_ResultFlag_IDX                    = 128,
    SBK_QFlags_QGestureRecognizer_ResultFlag_IDX             = 83,
    SBK_QGestureRecognizer_IDX                               = 127,
    SBK_QGraphicsAnchor_IDX                                  = 129,
    SBK_QGraphicsAnchorLayout_IDX                            = 130,
    SBK_QGraphicsBlurEffect_BlurHint_IDX                     = 132,
    SBK_QFlags_QGraphicsBlurEffect_BlurHint_IDX              = 84,
    SBK_QGraphicsBlurEffect_IDX                              = 131,
    SBK_QGraphicsColorizeEffect_IDX                          = 133,
    SBK_QGraphicsDropShadowEffect_IDX                        = 134,
    SBK_QGraphicsEffect_ChangeFlag_IDX                       = 136,
    SBK_QFlags_QGraphicsEffect_ChangeFlag_IDX                = 85,
    SBK_QGraphicsEffect_PixmapPadMode_IDX                    = 137,
    SBK_QGraphicsEffect_IDX                                  = 135,
    SBK_QGraphicsEllipseItem_IDX                             = 138,
    SBK_QGraphicsGridLayout_IDX                              = 139,
    SBK_QGraphicsItem_GraphicsItemFlag_IDX                   = 144,
    SBK_QFlags_QGraphicsItem_GraphicsItemFlag_IDX            = 86,
    SBK_QGraphicsItem_GraphicsItemChange_IDX                 = 143,
    SBK_QGraphicsItem_CacheMode_IDX                          = 141,
    SBK_QGraphicsItem_PanelModality_IDX                      = 145,
    SBK_QGraphicsItem_Extension_IDX                          = 142,
    SBK_QGraphicsItem_IDX                                    = 140,
    SBK_QGraphicsItemAnimation_IDX                           = 146,
    SBK_QGraphicsItemGroup_IDX                               = 147,
    SBK_QGraphicsLayout_IDX                                  = 148,
    SBK_QGraphicsLayoutItem_IDX                              = 149,
    SBK_QGraphicsLineItem_IDX                                = 150,
    SBK_QGraphicsLinearLayout_IDX                            = 151,
    SBK_QGraphicsObject_IDX                                  = 152,
    SBK_QGraphicsOpacityEffect_IDX                           = 153,
    SBK_QGraphicsPathItem_IDX                                = 154,
    SBK_QGraphicsPixmapItem_ShapeMode_IDX                    = 156,
    SBK_QGraphicsPixmapItem_IDX                              = 155,
    SBK_QGraphicsPolygonItem_IDX                             = 157,
    SBK_QGraphicsProxyWidget_IDX                             = 158,
    SBK_QGraphicsRectItem_IDX                                = 159,
    SBK_QGraphicsRotation_IDX                                = 160,
    SBK_QGraphicsScale_IDX                                   = 161,
    SBK_QGraphicsScene_ItemIndexMethod_IDX                   = 163,
    SBK_QGraphicsScene_SceneLayer_IDX                        = 164,
    SBK_QFlags_QGraphicsScene_SceneLayer_IDX                 = 87,
    SBK_QGraphicsScene_IDX                                   = 162,
    SBK_QGraphicsSceneContextMenuEvent_Reason_IDX            = 166,
    SBK_QGraphicsSceneContextMenuEvent_IDX                   = 165,
    SBK_QGraphicsSceneDragDropEvent_IDX                      = 167,
    SBK_QGraphicsSceneEvent_IDX                              = 168,
    SBK_QGraphicsSceneHelpEvent_IDX                          = 169,
    SBK_QGraphicsSceneHoverEvent_IDX                         = 170,
    SBK_QGraphicsSceneMouseEvent_IDX                         = 171,
    SBK_QGraphicsSceneMoveEvent_IDX                          = 172,
    SBK_QGraphicsSceneResizeEvent_IDX                        = 173,
    SBK_QGraphicsSceneWheelEvent_IDX                         = 174,
    SBK_QGraphicsSimpleTextItem_IDX                          = 175,
    SBK_QGraphicsTextItem_IDX                                = 176,
    SBK_QGraphicsTransform_IDX                               = 177,
    SBK_QGraphicsView_ViewportAnchor_IDX                     = 182,
    SBK_QGraphicsView_CacheModeFlag_IDX                      = 179,
    SBK_QFlags_QGraphicsView_CacheModeFlag_IDX               = 88,
    SBK_QGraphicsView_DragMode_IDX                           = 180,
    SBK_QGraphicsView_ViewportUpdateMode_IDX                 = 183,
    SBK_QGraphicsView_OptimizationFlag_IDX                   = 181,
    SBK_QFlags_QGraphicsView_OptimizationFlag_IDX            = 89,
    SBK_QGraphicsView_IDX                                    = 178,
    SBK_QGraphicsWidget_IDX                                  = 184,
    SBK_QGridLayout_IDX                                      = 185,
    SBK_QGroupBox_IDX                                        = 186,
    SBK_QHBoxLayout_IDX                                      = 187,
    SBK_QHeaderView_ResizeMode_IDX                           = 189,
    SBK_QHeaderView_IDX                                      = 188,
    SBK_QInputDialog_InputDialogOption_IDX                   = 191,
    SBK_QInputDialog_InputMode_IDX                           = 192,
    SBK_QInputDialog_IDX                                     = 190,
    SBK_QItemDelegate_IDX                                    = 193,
    SBK_QItemEditorCreatorBase_IDX                           = 194,
    SBK_QItemEditorFactory_IDX                               = 195,
    SBK_QKeySequenceEdit_IDX                                 = 196,
    SBK_QLCDNumber_Mode_IDX                                  = 198,
    SBK_QLCDNumber_SegmentStyle_IDX                          = 199,
    SBK_QLCDNumber_IDX                                       = 197,
    SBK_QLabel_IDX                                           = 200,
    SBK_QLayout_SizeConstraint_IDX                           = 202,
    SBK_QLayout_IDX                                          = 201,
    SBK_QLayoutItem_IDX                                      = 203,
    SBK_QLineEdit_ActionPosition_IDX                         = 205,
    SBK_QLineEdit_EchoMode_IDX                               = 206,
    SBK_QLineEdit_IDX                                        = 204,
    SBK_QListView_Movement_IDX                               = 210,
    SBK_QListView_Flow_IDX                                   = 208,
    SBK_QListView_ResizeMode_IDX                             = 211,
    SBK_QListView_LayoutMode_IDX                             = 209,
    SBK_QListView_ViewMode_IDX                               = 212,
    SBK_QListView_IDX                                        = 207,
    SBK_QListWidget_IDX                                      = 213,
    SBK_QListWidgetItem_ItemType_IDX                         = 215,
    SBK_QListWidgetItem_IDX                                  = 214,
    SBK_QMainWindow_DockOption_IDX                           = 217,
    SBK_QFlags_QMainWindow_DockOption_IDX                    = 90,
    SBK_QMainWindow_IDX                                      = 216,
    SBK_QMdiArea_AreaOption_IDX                              = 219,
    SBK_QFlags_QMdiArea_AreaOption_IDX                       = 91,
    SBK_QMdiArea_WindowOrder_IDX                             = 221,
    SBK_QMdiArea_ViewMode_IDX                                = 220,
    SBK_QMdiArea_IDX                                         = 218,
    SBK_QMdiSubWindow_SubWindowOption_IDX                    = 223,
    SBK_QFlags_QMdiSubWindow_SubWindowOption_IDX             = 92,
    SBK_QMdiSubWindow_IDX                                    = 222,
    SBK_QMenu_IDX                                            = 224,
    SBK_QMenuBar_IDX                                         = 225,
    SBK_QMessageBox_Option_IDX                               = 229,
    SBK_QFlags_QMessageBox_Option_IDX                        = 93,
    SBK_QMessageBox_Icon_IDX                                 = 228,
    SBK_QMessageBox_ButtonRole_IDX                           = 227,
    SBK_QMessageBox_StandardButton_IDX                       = 230,
    SBK_QFlags_QMessageBox_StandardButton_IDX                = 94,
    SBK_QMessageBox_IDX                                      = 226,
    SBK_QPanGesture_IDX                                      = 231,
    SBK_QPinchGesture_ChangeFlag_IDX                         = 233,
    SBK_QFlags_QPinchGesture_ChangeFlag_IDX                  = 95,
    SBK_QPinchGesture_IDX                                    = 232,
    SBK_QPlainTextDocumentLayout_IDX                         = 234,
    SBK_QPlainTextEdit_LineWrapMode_IDX                      = 236,
    SBK_QPlainTextEdit_IDX                                   = 235,
    SBK_QProgressBar_Direction_IDX                           = 238,
    SBK_QProgressBar_IDX                                     = 237,
    SBK_QProgressDialog_IDX                                  = 239,
    SBK_QProxyStyle_IDX                                      = 240,
    SBK_QPushButton_IDX                                      = 241,
    SBK_QRadioButton_IDX                                     = 242,
    SBK_QRhiWidget_Api_IDX                                   = 244,
    SBK_QRhiWidget_TextureFormat_IDX                         = 245,
    SBK_QRhiWidget_IDX                                       = 243,
    SBK_QRubberBand_Shape_IDX                                = 247,
    SBK_QRubberBand_IDX                                      = 246,
    SBK_QScrollArea_IDX                                      = 248,
    SBK_QScrollBar_IDX                                       = 249,
    SBK_QScroller_State_IDX                                  = 253,
    SBK_QScroller_ScrollerGestureType_IDX                    = 252,
    SBK_QScroller_Input_IDX                                  = 251,
    SBK_QScroller_IDX                                        = 250,
    SBK_QScrollerProperties_OvershootPolicy_IDX              = 256,
    SBK_QScrollerProperties_FrameRates_IDX                   = 255,
    SBK_QScrollerProperties_ScrollMetric_IDX                 = 257,
    SBK_QScrollerProperties_IDX                              = 254,
    SBK_QSizeGrip_IDX                                        = 258,
    SBK_QSizePolicy_PolicyFlag_IDX                           = 262,
    SBK_QSizePolicy_Policy_IDX                               = 261,
    SBK_QSizePolicy_ControlType_IDX                          = 260,
    SBK_QFlags_QSizePolicy_ControlType_IDX                   = 96,
    SBK_QSizePolicy_IDX                                      = 259,
    SBK_QSlider_TickPosition_IDX                             = 264,
    SBK_QSlider_IDX                                          = 263,
    SBK_QSpacerItem_IDX                                      = 265,
    SBK_QSpinBox_IDX                                         = 266,
    SBK_QSplashScreen_IDX                                    = 267,
    SBK_QSplitter_IDX                                        = 268,
    SBK_QSplitterHandle_IDX                                  = 269,
    SBK_QStackedLayout_StackingMode_IDX                      = 271,
    SBK_QStackedLayout_IDX                                   = 270,
    SBK_QStackedWidget_IDX                                   = 272,
    SBK_QStatusBar_IDX                                       = 273,
    SBK_QStyle_StateFlag_IDX                                 = 282,
    SBK_QFlags_QStyle_StateFlag_IDX                          = 97,
    SBK_QStyle_PrimitiveElement_IDX                          = 279,
    SBK_QStyle_ControlElement_IDX                            = 277,
    SBK_QStyle_SubElement_IDX                                = 285,
    SBK_QStyle_ComplexControl_IDX                            = 275,
    SBK_QStyle_SubControl_IDX                                = 284,
    SBK_QFlags_QStyle_SubControl_IDX                         = 98,
    SBK_QStyle_PixelMetric_IDX                               = 278,
    SBK_QStyle_ContentsType_IDX                              = 276,
    SBK_QStyle_RequestSoftwareInputPanel_IDX                 = 280,
    SBK_QStyle_StyleHint_IDX                                 = 283,
    SBK_QStyle_StandardPixmap_IDX                            = 281,
    SBK_QStyle_IDX                                           = 274,
    SBK_QStyleFactory_IDX                                    = 286,
    SBK_QStyleHintReturn_HintReturnType_IDX                  = 288,
    SBK_QStyleHintReturn_StyleOptionType_IDX                 = 289,
    SBK_QStyleHintReturn_StyleOptionVersion_IDX              = 290,
    SBK_QStyleHintReturn_IDX                                 = 287,
    SBK_QStyleHintReturnMask_StyleOptionType_IDX             = 292,
    SBK_QStyleHintReturnMask_StyleOptionVersion_IDX          = 293,
    SBK_QStyleHintReturnMask_IDX                             = 291,
    SBK_QStyleHintReturnVariant_StyleOptionType_IDX          = 295,
    SBK_QStyleHintReturnVariant_StyleOptionVersion_IDX       = 296,
    SBK_QStyleHintReturnVariant_IDX                          = 294,
    SBK_QStyleOption_OptionType_IDX                          = 298,
    SBK_QStyleOption_StyleOptionType_IDX                     = 299,
    SBK_QStyleOption_StyleOptionVersion_IDX                  = 300,
    SBK_QStyleOption_IDX                                     = 297,
    SBK_QStyleOptionButton_StyleOptionType_IDX               = 303,
    SBK_QStyleOptionButton_StyleOptionVersion_IDX            = 304,
    SBK_QStyleOptionButton_ButtonFeature_IDX                 = 302,
    SBK_QFlags_QStyleOptionButton_ButtonFeature_IDX          = 99,
    SBK_QStyleOptionButton_IDX                               = 301,
    SBK_QStyleOptionComboBox_StyleOptionType_IDX             = 306,
    SBK_QStyleOptionComboBox_StyleOptionVersion_IDX          = 307,
    SBK_QStyleOptionComboBox_IDX                             = 305,
    SBK_QStyleOptionComplex_StyleOptionType_IDX              = 309,
    SBK_QStyleOptionComplex_StyleOptionVersion_IDX           = 310,
    SBK_QStyleOptionComplex_IDX                              = 308,
    SBK_QStyleOptionDockWidget_StyleOptionType_IDX           = 312,
    SBK_QStyleOptionDockWidget_StyleOptionVersion_IDX        = 313,
    SBK_QStyleOptionDockWidget_IDX                           = 311,
    SBK_QStyleOptionFocusRect_StyleOptionType_IDX            = 315,
    SBK_QStyleOptionFocusRect_StyleOptionVersion_IDX         = 316,
    SBK_QStyleOptionFocusRect_IDX                            = 314,
    SBK_QStyleOptionFrame_StyleOptionType_IDX                = 319,
    SBK_QStyleOptionFrame_StyleOptionVersion_IDX             = 320,
    SBK_QStyleOptionFrame_FrameFeature_IDX                   = 318,
    SBK_QFlags_QStyleOptionFrame_FrameFeature_IDX            = 100,
    SBK_QStyleOptionFrame_IDX                                = 317,
    SBK_QStyleOptionGraphicsItem_StyleOptionType_IDX         = 322,
    SBK_QStyleOptionGraphicsItem_StyleOptionVersion_IDX      = 323,
    SBK_QStyleOptionGraphicsItem_IDX                         = 321,
    SBK_QStyleOptionGroupBox_StyleOptionType_IDX             = 325,
    SBK_QStyleOptionGroupBox_StyleOptionVersion_IDX          = 326,
    SBK_QStyleOptionGroupBox_IDX                             = 324,
    SBK_QStyleOptionHeader_StyleOptionType_IDX               = 331,
    SBK_QStyleOptionHeader_StyleOptionVersion_IDX            = 332,
    SBK_QStyleOptionHeader_SectionPosition_IDX               = 328,
    SBK_QStyleOptionHeader_SelectedPosition_IDX              = 329,
    SBK_QStyleOptionHeader_SortIndicator_IDX                 = 330,
    SBK_QStyleOptionHeader_IDX                               = 327,
    SBK_QStyleOptionHeaderV2_StyleOptionType_IDX             = 334,
    SBK_QStyleOptionHeaderV2_StyleOptionVersion_IDX          = 335,
    SBK_QStyleOptionHeaderV2_IDX                             = 333,
    SBK_QStyleOptionMenuItem_StyleOptionType_IDX             = 339,
    SBK_QStyleOptionMenuItem_StyleOptionVersion_IDX          = 340,
    SBK_QStyleOptionMenuItem_MenuItemType_IDX                = 338,
    SBK_QStyleOptionMenuItem_CheckType_IDX                   = 337,
    SBK_QStyleOptionMenuItem_IDX                             = 336,
    SBK_QStyleOptionProgressBar_StyleOptionType_IDX          = 342,
    SBK_QStyleOptionProgressBar_StyleOptionVersion_IDX       = 343,
    SBK_QStyleOptionProgressBar_IDX                          = 341,
    SBK_QStyleOptionRubberBand_StyleOptionType_IDX           = 345,
    SBK_QStyleOptionRubberBand_StyleOptionVersion_IDX        = 346,
    SBK_QStyleOptionRubberBand_IDX                           = 344,
    SBK_QStyleOptionSizeGrip_StyleOptionType_IDX             = 348,
    SBK_QStyleOptionSizeGrip_StyleOptionVersion_IDX          = 349,
    SBK_QStyleOptionSizeGrip_IDX                             = 347,
    SBK_QStyleOptionSlider_StyleOptionType_IDX               = 351,
    SBK_QStyleOptionSlider_StyleOptionVersion_IDX            = 352,
    SBK_QStyleOptionSlider_IDX                               = 350,
    SBK_QStyleOptionSpinBox_StyleOptionType_IDX              = 354,
    SBK_QStyleOptionSpinBox_StyleOptionVersion_IDX           = 355,
    SBK_QStyleOptionSpinBox_IDX                              = 353,
    SBK_QStyleOptionTab_StyleOptionType_IDX                  = 359,
    SBK_QStyleOptionTab_StyleOptionVersion_IDX               = 360,
    SBK_QStyleOptionTab_TabPosition_IDX                      = 362,
    SBK_QStyleOptionTab_SelectedPosition_IDX                 = 358,
    SBK_QStyleOptionTab_CornerWidget_IDX                     = 357,
    SBK_QFlags_QStyleOptionTab_CornerWidget_IDX              = 101,
    SBK_QStyleOptionTab_TabFeature_IDX                       = 361,
    SBK_QFlags_QStyleOptionTab_TabFeature_IDX                = 102,
    SBK_QStyleOptionTab_IDX                                  = 356,
    SBK_QStyleOptionTabBarBase_StyleOptionType_IDX           = 364,
    SBK_QStyleOptionTabBarBase_StyleOptionVersion_IDX        = 365,
    SBK_QStyleOptionTabBarBase_IDX                           = 363,
    SBK_QStyleOptionTabWidgetFrame_StyleOptionType_IDX       = 367,
    SBK_QStyleOptionTabWidgetFrame_StyleOptionVersion_IDX    = 368,
    SBK_QStyleOptionTabWidgetFrame_IDX                       = 366,
    SBK_QStyleOptionTitleBar_StyleOptionType_IDX             = 370,
    SBK_QStyleOptionTitleBar_StyleOptionVersion_IDX          = 371,
    SBK_QStyleOptionTitleBar_IDX                             = 369,
    SBK_QStyleOptionToolBar_StyleOptionType_IDX              = 373,
    SBK_QStyleOptionToolBar_StyleOptionVersion_IDX           = 374,
    SBK_QStyleOptionToolBar_ToolBarPosition_IDX              = 376,
    SBK_QStyleOptionToolBar_ToolBarFeature_IDX               = 375,
    SBK_QFlags_QStyleOptionToolBar_ToolBarFeature_IDX        = 103,
    SBK_QStyleOptionToolBar_IDX                              = 372,
    SBK_QStyleOptionToolBox_StyleOptionType_IDX              = 379,
    SBK_QStyleOptionToolBox_StyleOptionVersion_IDX           = 380,
    SBK_QStyleOptionToolBox_TabPosition_IDX                  = 381,
    SBK_QStyleOptionToolBox_SelectedPosition_IDX             = 378,
    SBK_QStyleOptionToolBox_IDX                              = 377,
    SBK_QStyleOptionToolButton_StyleOptionType_IDX           = 383,
    SBK_QStyleOptionToolButton_StyleOptionVersion_IDX        = 384,
    SBK_QStyleOptionToolButton_ToolButtonFeature_IDX         = 385,
    SBK_QFlags_QStyleOptionToolButton_ToolButtonFeature_IDX  = 104,
    SBK_QStyleOptionToolButton_IDX                           = 382,
    SBK_QStyleOptionViewItem_StyleOptionType_IDX             = 388,
    SBK_QStyleOptionViewItem_StyleOptionVersion_IDX          = 389,
    SBK_QStyleOptionViewItem_Position_IDX                    = 387,
    SBK_QStyleOptionViewItem_ViewItemFeature_IDX             = 390,
    SBK_QFlags_QStyleOptionViewItem_ViewItemFeature_IDX      = 105,
    SBK_QStyleOptionViewItem_ViewItemPosition_IDX            = 391,
    SBK_QStyleOptionViewItem_IDX                             = 386,
    SBK_QStylePainter_IDX                                    = 392,
    SBK_QStyledItemDelegate_IDX                              = 393,
    SBK_QSwipeGesture_SwipeDirection_IDX                     = 395,
    SBK_QSwipeGesture_IDX                                    = 394,
    SBK_QSystemTrayIcon_ActivationReason_IDX                 = 397,
    SBK_QSystemTrayIcon_MessageIcon_IDX                      = 398,
    SBK_QSystemTrayIcon_IDX                                  = 396,
    SBK_QTabBar_Shape_IDX                                    = 402,
    SBK_QTabBar_ButtonPosition_IDX                           = 400,
    SBK_QTabBar_SelectionBehavior_IDX                        = 401,
    SBK_QTabBar_IDX                                          = 399,
    SBK_QTabWidget_TabPosition_IDX                           = 404,
    SBK_QTabWidget_TabShape_IDX                              = 405,
    SBK_QTabWidget_IDX                                       = 403,
    SBK_QTableView_IDX                                       = 406,
    SBK_QTableWidget_IDX                                     = 407,
    SBK_QTableWidgetItem_ItemType_IDX                        = 409,
    SBK_QTableWidgetItem_IDX                                 = 408,
    SBK_QTableWidgetSelectionRange_IDX                       = 410,
    SBK_QTapAndHoldGesture_IDX                               = 411,
    SBK_QTapGesture_IDX                                      = 412,
    SBK_QTextBrowser_IDX                                     = 413,
    SBK_QTextEdit_LineWrapMode_IDX                           = 417,
    SBK_QTextEdit_AutoFormattingFlag_IDX                     = 415,
    SBK_QFlags_QTextEdit_AutoFormattingFlag_IDX              = 106,
    SBK_QTextEdit_IDX                                        = 414,
    SBK_QTextEdit_ExtraSelection_IDX                         = 416,
    SBK_QTileRules_IDX                                       = 418,
    SBK_QTimeEdit_IDX                                        = 419,
    SBK_QToolBar_IDX                                         = 420,
    SBK_QToolBox_IDX                                         = 421,
    SBK_QToolButton_ToolButtonPopupMode_IDX                  = 423,
    SBK_QToolButton_IDX                                      = 422,
    SBK_QToolTip_IDX                                         = 424,
    SBK_QTreeView_IDX                                        = 425,
    SBK_QTreeWidget_IDX                                      = 426,
    SBK_QTreeWidgetItem_ItemType_IDX                         = 429,
    SBK_QTreeWidgetItem_ChildIndicatorPolicy_IDX             = 428,
    SBK_QTreeWidgetItem_IDX                                  = 427,
    SBK_QTreeWidgetItemIterator_IteratorFlag_IDX             = 431,
    SBK_QFlags_QTreeWidgetItemIterator_IteratorFlag_IDX      = 107,
    SBK_QTreeWidgetItemIterator_IDX                          = 430,
    SBK_QUndoView_IDX                                        = 432,
    SBK_QVBoxLayout_IDX                                      = 433,
    SBK_QWhatsThis_IDX                                       = 434,
    SBK_QWidget_RenderFlag_IDX                               = 436,
    SBK_QFlags_QWidget_RenderFlag_IDX                        = 108,
    SBK_QWidget_IDX                                          = 435,
    SBK_QWidgetAction_IDX                                    = 437,
    SBK_QWidgetItem_IDX                                      = 438,
    SBK_QWizard_WizardButton_IDX                             = 440,
    SBK_QWizard_WizardPixmap_IDX                             = 442,
    SBK_QWizard_WizardStyle_IDX                              = 443,
    SBK_QWizard_WizardOption_IDX                             = 441,
    SBK_QFlags_QWizard_WizardOption_IDX                      = 109,
    SBK_QWizard_IDX                                          = 439,
    SBK_QWizardPage_IDX                                      = 444,
    SBK_QtWidgets_IDX_COUNT                                  = 445,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtWidgetsTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtWidgetsTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtWidgetsModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtWidgetsTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTWIDGETS_QLIST_INT_IDX                              = 0, // QList<int>
    SBK_QTWIDGETS_QLIST_QTREEWIDGETITEMPTR_IDX               = 2, // QList<QTreeWidgetItem*>
    SBK_QTWIDGETS_QLIST_QCOLOR_IDX                           = 4, // QList<QColor>
    SBK_QTWIDGETS_STD_PAIR_QACCESSIBLEINTERFACEPTR_QFLAGS_QACCESSIBLE_RELATIONFLAG_IDX = 6, // std::pair<QAccessibleInterface*,QFlags<QAccessible::RelationFlag>>
    SBK_QTWIDGETS_QLIST_STD_PAIR_QACCESSIBLEINTERFACEPTR_QFLAGS_QACCESSIBLE_RELATIONFLAG_IDX = 8, // QList<std::pair<QAccessibleInterface*,QFlags<QAccessible::RelationFlag>>>
    SBK_QTWIDGETS_QLIST_QGRAPHICSITEMPTR_IDX                 = 10, // QList<QGraphicsItem*>
    SBK_QTWIDGETS_QLIST_QGRAPHICSTRANSFORMPTR_IDX            = 12, // QList<QGraphicsTransform*>
    SBK_QTWIDGETS_QLIST_QLINE_IDX                            = 14, // QList<QLine>
    SBK_QTWIDGETS_QLIST_QLINEF_IDX                           = 16, // QList<QLineF>
    SBK_QTWIDGETS_QLIST_QPOINT_IDX                           = 18, // QList<QPoint>
    SBK_QTWIDGETS_QLIST_QPOINTF_IDX                          = 20, // QList<QPointF>
    SBK_QTWIDGETS_QLIST_QRECT_IDX                            = 22, // QList<QRect>
    SBK_QTWIDGETS_QLIST_QRECTF_IDX                           = 24, // QList<QRectF>
    SBK_QTWIDGETS_QLIST_QACTIONPTR_IDX                       = 26, // QList<QAction*>
    SBK_QTWIDGETS_QLIST_QOBJECTPTR_IDX                       = 28, // QList<QObject*>
    SBK_QTWIDGETS_QLIST_QBYTEARRAY_IDX                       = 30, // QList<QByteArray>
    SBK_QTWIDGETS_QLIST_QDOCKWIDGETPTR_IDX                   = 32, // QList<QDockWidget*>
    SBK_QTWIDGETS_QLIST_QKEYCOMBINATION_IDX                  = 34, // QList<QKeyCombination>
    SBK_QTWIDGETS_QLIST_QWIDGETPTR_IDX                       = 36, // QList<QWidget*>
    SBK_QTWIDGETS_QLIST_QTEXTEDIT_EXTRASELECTION_IDX         = 38, // QList<QTextEdit::ExtraSelection>
    SBK_QTWIDGETS_QLIST_QMDISUBWINDOWPTR_IDX                 = 40, // QList<QMdiSubWindow*>
    SBK_QTWIDGETS_QLIST_QMODELINDEX_IDX                      = 42, // QList<QModelIndex>
    SBK_QTWIDGETS_QLIST_QTABLEWIDGETITEMPTR_IDX              = 44, // QList<QTableWidgetItem*>
    SBK_QTWIDGETS_QLIST_QTABLEWIDGETSELECTIONRANGE_IDX       = 46, // QList<QTableWidgetSelectionRange>
    SBK_QTWIDGETS_QLIST_QLISTWIDGETITEMPTR_IDX               = 48, // QList<QListWidgetItem*>
    SBK_QTWIDGETS_QLIST_QABSTRACTBUTTONPTR_IDX               = 50, // QList<QAbstractButton*>
    SBK_QTWIDGETS_QLIST_QWIZARD_WIZARDBUTTON_IDX             = 52, // QList<QWizard::WizardButton>
    SBK_QTWIDGETS_QMAP_QDATE_QTEXTCHARFORMAT_IDX             = 54, // QMap<QDate,QTextCharFormat>
    SBK_QTWIDGETS_QLIST_QSCROLLERPTR_IDX                     = 56, // QList<QScroller*>
    SBK_QTWIDGETS_QLIST_QREAL_IDX                            = 58, // QList<qreal>
    SBK_QTWIDGETS_QLIST_QGRAPHICSVIEWPTR_IDX                 = 60, // QList<QGraphicsView*>
    SBK_QTWIDGETS_STD_PAIR_QREAL_QPOINTF_IDX                 = 62, // std::pair<qreal,QPointF>
    SBK_QTWIDGETS_QLIST_STD_PAIR_QREAL_QPOINTF_IDX           = 64, // QList<std::pair<qreal,QPointF>>
    SBK_QTWIDGETS_STD_PAIR_QREAL_QREAL_IDX                   = 66, // std::pair<qreal,qreal>
    SBK_QTWIDGETS_QLIST_STD_PAIR_QREAL_QREAL_IDX             = 68, // QList<std::pair<qreal,qreal>>
    SBK_QTWIDGETS_QLIST_QKEYSEQUENCE_IDX                     = 70, // QList<QKeySequence>
    SBK_QTWIDGETS_QLIST_QGESTUREPTR_IDX                      = 72, // QList<QGesture*>
    SBK_QTWIDGETS_QLIST_QWINDOWPTR_IDX                       = 74, // QList<QWindow*>
    SBK_QTWIDGETS_QLIST_QSCREENPTR_IDX                       = 76, // QList<QScreen*>
    SBK_QTWIDGETS_QLIST_QURL_IDX                             = 78, // QList<QUrl>
    SBK_QTWIDGETS_QMAP_INT_QVARIANT_IDX                      = 80, // QMap<int,QVariant>
    SBK_QTWIDGETS_QHASH_INT_QBYTEARRAY_IDX                   = 82, // QHash<int,QByteArray>
    SBK_QTWIDGETS_QLIST_QVARIANT_IDX                         = 84, // QList<QVariant>
    SBK_QTWIDGETS_QLIST_QSTRING_IDX                          = 86, // QList<QString>
    SBK_QTWIDGETS_QMAP_QSTRING_QVARIANT_IDX                  = 88, // QMap<QString,QVariant>
    SBK_QTWIDGETS_CONVERTERS_IDX_COUNT                       = 90,
};

// Converter indices
enum : int {
    SBK_QtWidgets_QList_int_IDX                              = 0, // QList<int>
    SBK_QtWidgets_QList_QTreeWidgetItemPTR_IDX               = 1, // QList<QTreeWidgetItem*>
    SBK_QtWidgets_QList_QColor_IDX                           = 2, // QList<QColor>
    SBK_QtWidgets_std_pair_QAccessibleInterfacePTR_QFlags_QAccessible_RelationFlag_IDX = 3, // std::pair<QAccessibleInterface*,QFlags<QAccessible::RelationFlag>>
    SBK_QtWidgets_QList_std_pair_QAccessibleInterfacePTR_QFlags_QAccessible_RelationFlag_IDX = 4, // QList<std::pair<QAccessibleInterface*,QFlags<QAccessible::RelationFlag>>>
    SBK_QtWidgets_QList_QGraphicsItemPTR_IDX                 = 5, // QList<QGraphicsItem*>
    SBK_QtWidgets_QList_QGraphicsTransformPTR_IDX            = 6, // QList<QGraphicsTransform*>
    SBK_QtWidgets_QList_QLine_IDX                            = 7, // QList<QLine>
    SBK_QtWidgets_QList_QLineF_IDX                           = 8, // QList<QLineF>
    SBK_QtWidgets_QList_QPoint_IDX                           = 9, // QList<QPoint>
    SBK_QtWidgets_QList_QPointF_IDX                          = 10, // QList<QPointF>
    SBK_QtWidgets_QList_QRect_IDX                            = 11, // QList<QRect>
    SBK_QtWidgets_QList_QRectF_IDX                           = 12, // QList<QRectF>
    SBK_QtWidgets_QList_QActionPTR_IDX                       = 13, // QList<QAction*>
    SBK_QtWidgets_QList_QObjectPTR_IDX                       = 14, // QList<QObject*>
    SBK_QtWidgets_QList_QByteArray_IDX                       = 15, // QList<QByteArray>
    SBK_QtWidgets_QList_QDockWidgetPTR_IDX                   = 16, // QList<QDockWidget*>
    SBK_QtWidgets_QList_QKeyCombination_IDX                  = 17, // QList<QKeyCombination>
    SBK_QtWidgets_QList_QWidgetPTR_IDX                       = 18, // QList<QWidget*>
    SBK_QtWidgets_QList_QTextEdit_ExtraSelection_IDX         = 19, // QList<QTextEdit::ExtraSelection>
    SBK_QtWidgets_QList_QMdiSubWindowPTR_IDX                 = 20, // QList<QMdiSubWindow*>
    SBK_QtWidgets_QList_QModelIndex_IDX                      = 21, // QList<QModelIndex>
    SBK_QtWidgets_QList_QTableWidgetItemPTR_IDX              = 22, // QList<QTableWidgetItem*>
    SBK_QtWidgets_QList_QTableWidgetSelectionRange_IDX       = 23, // QList<QTableWidgetSelectionRange>
    SBK_QtWidgets_QList_QListWidgetItemPTR_IDX               = 24, // QList<QListWidgetItem*>
    SBK_QtWidgets_QList_QAbstractButtonPTR_IDX               = 25, // QList<QAbstractButton*>
    SBK_QtWidgets_QList_QWizard_WizardButton_IDX             = 26, // QList<QWizard::WizardButton>
    SBK_QtWidgets_QMap_QDate_QTextCharFormat_IDX             = 27, // QMap<QDate,QTextCharFormat>
    SBK_QtWidgets_QList_QScrollerPTR_IDX                     = 28, // QList<QScroller*>
    SBK_QtWidgets_QList_qreal_IDX                            = 29, // QList<qreal>
    SBK_QtWidgets_QList_QGraphicsViewPTR_IDX                 = 30, // QList<QGraphicsView*>
    SBK_QtWidgets_std_pair_qreal_QPointF_IDX                 = 31, // std::pair<qreal,QPointF>
    SBK_QtWidgets_QList_std_pair_qreal_QPointF_IDX           = 32, // QList<std::pair<qreal,QPointF>>
    SBK_QtWidgets_std_pair_qreal_qreal_IDX                   = 33, // std::pair<qreal,qreal>
    SBK_QtWidgets_QList_std_pair_qreal_qreal_IDX             = 34, // QList<std::pair<qreal,qreal>>
    SBK_QtWidgets_QList_QKeySequence_IDX                     = 35, // QList<QKeySequence>
    SBK_QtWidgets_QList_QGesturePTR_IDX                      = 36, // QList<QGesture*>
    SBK_QtWidgets_QList_QWindowPTR_IDX                       = 37, // QList<QWindow*>
    SBK_QtWidgets_QList_QScreenPTR_IDX                       = 38, // QList<QScreen*>
    SBK_QtWidgets_QList_QUrl_IDX                             = 39, // QList<QUrl>
    SBK_QtWidgets_QMap_int_QVariant_IDX                      = 40, // QMap<int,QVariant>
    SBK_QtWidgets_QHash_int_QByteArray_IDX                   = 41, // QHash<int,QByteArray>
    SBK_QtWidgets_QList_QVariant_IDX                         = 42, // QList<QVariant>
    SBK_QtWidgets_QList_QString_IDX                          = 43, // QList<QString>
    SBK_QtWidgets_QMap_QString_QVariant_IDX                  = 44, // QMap<QString,QVariant>
    SBK_QtWidgets_CONVERTERS_IDX_COUNT                       = 45,
};
// Macros for type check

// Protected enum surrogates
enum PySide6_QtWidgets_QAbstractItemView_CursorAction_Surrogate : int {};
enum PySide6_QtWidgets_QAbstractItemView_State_Surrogate : int {};
enum PySide6_QtWidgets_QAbstractItemView_DropIndicatorPosition_Surrogate : int {};
enum PySide6_QtWidgets_QAbstractSlider_SliderChange_Surrogate : int {};
enum PySide6_QtWidgets_QGraphicsItem_Extension_Surrogate : int {};

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QAbstractButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractGraphicsShapeItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractGraphicsShapeItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemDelegate::EndEditHint >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemDelegate_EndEditHint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemDelegate >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemDelegate_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemView::SelectionMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_SelectionMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemView::SelectionBehavior >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_SelectionBehavior_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemView::ScrollHint >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_ScrollHint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemView::EditTrigger >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_EditTrigger_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QAbstractItemView::EditTrigger> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QAbstractItemView_EditTrigger_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemView::ScrollMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_ScrollMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemView::DragDropMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_DragDropMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::PySide6_QtWidgets_QAbstractItemView_CursorAction_Surrogate >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_CursorAction_IDX]); }
template<> inline PyTypeObject *SbkType< ::PySide6_QtWidgets_QAbstractItemView_State_Surrogate >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_State_IDX]); }
template<> inline PyTypeObject *SbkType< ::PySide6_QtWidgets_QAbstractItemView_DropIndicatorPosition_Surrogate >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_DropIndicatorPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractItemView >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractItemView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractScrollArea::SizeAdjustPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractScrollArea_SizeAdjustPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractScrollArea >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractScrollArea_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSlider::SliderAction >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractSlider_SliderAction_IDX]); }
template<> inline PyTypeObject *SbkType< ::PySide6_QtWidgets_QAbstractSlider_SliderChange_Surrogate >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractSlider_SliderChange_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSlider >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractSlider_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSpinBox::StepEnabledFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractSpinBox_StepEnabledFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QAbstractSpinBox::StepEnabledFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QAbstractSpinBox_StepEnabledFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSpinBox::ButtonSymbols >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractSpinBox_ButtonSymbols_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSpinBox::CorrectionMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractSpinBox_CorrectionMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSpinBox::StepType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractSpinBox_StepType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSpinBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAbstractSpinBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAccessibleWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QAccessibleWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QApplication >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QApplication_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBoxLayout::Direction >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QBoxLayout_Direction_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBoxLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QBoxLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QButtonGroup >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QButtonGroup_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCalendarWidget::HorizontalHeaderFormat >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCalendarWidget_HorizontalHeaderFormat_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCalendarWidget::VerticalHeaderFormat >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCalendarWidget_VerticalHeaderFormat_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCalendarWidget::SelectionMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCalendarWidget_SelectionMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCalendarWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCalendarWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCheckBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCheckBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QColorDialog::ColorDialogOption >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QColorDialog_ColorDialogOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QColorDialog::ColorDialogOption> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QColorDialog_ColorDialogOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QColorDialog >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QColorDialog_IDX]); }
template<> inline PyTypeObject *SbkType< ::QColormap::Mode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QColormap_Mode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QColormap >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QColormap_IDX]); }
template<> inline PyTypeObject *SbkType< ::QColumnView >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QColumnView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QComboBox::InsertPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QComboBox_InsertPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QComboBox::SizeAdjustPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QComboBox_SizeAdjustPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QComboBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QComboBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCommandLinkButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCommandLinkButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCommonStyle >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCommonStyle_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCompleter::CompletionMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCompleter_CompletionMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCompleter::ModelSorting >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCompleter_ModelSorting_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCompleter >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QCompleter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDataWidgetMapper::SubmitPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDataWidgetMapper_SubmitPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDataWidgetMapper >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDataWidgetMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDateEdit >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDateEdit_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDateTimeEdit::Section >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDateTimeEdit_Section_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QDateTimeEdit::Section> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QDateTimeEdit_Section_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDateTimeEdit >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDateTimeEdit_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDial >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDial_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDialog::DialogCode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDialog_DialogCode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDialog >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDialog_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDialogButtonBox::ButtonRole >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDialogButtonBox_ButtonRole_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDialogButtonBox::StandardButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDialogButtonBox_StandardButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QDialogButtonBox::StandardButton> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QDialogButtonBox_StandardButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDialogButtonBox::ButtonLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDialogButtonBox_ButtonLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDialogButtonBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDialogButtonBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDockWidget::DockWidgetFeature >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDockWidget_DockWidgetFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QDockWidget::DockWidgetFeature> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QDockWidget_DockWidgetFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDockWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDockWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDoubleSpinBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QDoubleSpinBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QErrorMessage >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QErrorMessage_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileDialog::ViewMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileDialog_ViewMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileDialog::FileMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileDialog_FileMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileDialog::AcceptMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileDialog_AcceptMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileDialog::DialogLabel >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileDialog_DialogLabel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileDialog::Option >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileDialog_Option_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QFileDialog::Option> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QFileDialog_Option_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileDialog >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileDialog_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileIconProvider >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileIconProvider_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileSystemModel::Roles >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileSystemModel_Roles_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileSystemModel::Option >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileSystemModel_Option_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QFileSystemModel::Option> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QFileSystemModel_Option_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFileSystemModel >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFileSystemModel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFocusFrame >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFocusFrame_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFontComboBox::FontFilter >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFontComboBox_FontFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QFontComboBox::FontFilter> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QFontComboBox_FontFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFontComboBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFontComboBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFontDialog::FontDialogOption >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFontDialog_FontDialogOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QFontDialog::FontDialogOption> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QFontDialog_FontDialogOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFontDialog >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFontDialog_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFormLayout::FieldGrowthPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFormLayout_FieldGrowthPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFormLayout::RowWrapPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFormLayout_RowWrapPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFormLayout::ItemRole >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFormLayout_ItemRole_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFormLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFormLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFormLayout::TakeRowResult >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFormLayout_TakeRowResult_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFrame::Shape >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFrame_Shape_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFrame::Shadow >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFrame_Shadow_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFrame::StyleMask >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFrame_StyleMask_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFrame >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFrame_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGesture::GestureCancelPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGesture_GestureCancelPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGesture >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGesture_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGestureEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGestureEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGestureRecognizer::ResultFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGestureRecognizer_ResultFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGestureRecognizer::ResultFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QGestureRecognizer_ResultFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGestureRecognizer >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGestureRecognizer_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsAnchor >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsAnchor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsAnchorLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsAnchorLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsBlurEffect::BlurHint >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsBlurEffect_BlurHint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGraphicsBlurEffect::BlurHint> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QGraphicsBlurEffect_BlurHint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsBlurEffect >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsBlurEffect_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsColorizeEffect >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsColorizeEffect_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsDropShadowEffect >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsDropShadowEffect_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsEffect::ChangeFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsEffect_ChangeFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGraphicsEffect::ChangeFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QGraphicsEffect_ChangeFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsEffect::PixmapPadMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsEffect_PixmapPadMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsEffect >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsEffect_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsEllipseItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsEllipseItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsGridLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsGridLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsItem::GraphicsItemFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsItem_GraphicsItemFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGraphicsItem::GraphicsItemFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QGraphicsItem_GraphicsItemFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsItem::GraphicsItemChange >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsItem_GraphicsItemChange_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsItem::CacheMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsItem_CacheMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsItem::PanelModality >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsItem_PanelModality_IDX]); }
template<> inline PyTypeObject *SbkType< ::PySide6_QtWidgets_QGraphicsItem_Extension_Surrogate >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsItem_Extension_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsItemAnimation >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsItemAnimation_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsItemGroup >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsItemGroup_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsLayoutItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsLayoutItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsLineItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsLineItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsLinearLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsLinearLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsObject >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsObject_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsOpacityEffect >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsOpacityEffect_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsPathItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsPathItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsPixmapItem::ShapeMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsPixmapItem_ShapeMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsPixmapItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsPixmapItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsPolygonItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsPolygonItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsProxyWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsProxyWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsRectItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsRectItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsRotation >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsRotation_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsScale >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsScale_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsScene::ItemIndexMethod >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsScene_ItemIndexMethod_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsScene::SceneLayer >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsScene_SceneLayer_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGraphicsScene::SceneLayer> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QGraphicsScene_SceneLayer_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsScene >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsScene_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneContextMenuEvent::Reason >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneContextMenuEvent_Reason_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneContextMenuEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneContextMenuEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneDragDropEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneDragDropEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneHelpEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneHelpEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneHoverEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneHoverEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneMouseEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneMouseEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneMoveEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneMoveEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneResizeEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneResizeEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSceneWheelEvent >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSceneWheelEvent_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsSimpleTextItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsSimpleTextItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsTextItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsTextItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsTransform >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsTransform_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsView::ViewportAnchor >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsView_ViewportAnchor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsView::CacheModeFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsView_CacheModeFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGraphicsView::CacheModeFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QGraphicsView_CacheModeFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsView::DragMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsView_DragMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsView::ViewportUpdateMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsView_ViewportUpdateMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsView::OptimizationFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsView_OptimizationFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGraphicsView::OptimizationFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QGraphicsView_OptimizationFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsView >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGraphicsWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGraphicsWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGridLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGridLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGroupBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QGroupBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHBoxLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QHBoxLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHeaderView::ResizeMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QHeaderView_ResizeMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHeaderView >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QHeaderView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QInputDialog::InputDialogOption >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QInputDialog_InputDialogOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QInputDialog::InputMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QInputDialog_InputMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QInputDialog >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QInputDialog_IDX]); }
template<> inline PyTypeObject *SbkType< ::QItemDelegate >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QItemDelegate_IDX]); }
template<> inline PyTypeObject *SbkType< ::QItemEditorCreatorBase >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QItemEditorCreatorBase_IDX]); }
template<> inline PyTypeObject *SbkType< ::QItemEditorFactory >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QItemEditorFactory_IDX]); }
template<> inline PyTypeObject *SbkType< ::QKeySequenceEdit >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QKeySequenceEdit_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLCDNumber::Mode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLCDNumber_Mode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLCDNumber::SegmentStyle >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLCDNumber_SegmentStyle_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLCDNumber >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLCDNumber_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLabel >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLabel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLayout::SizeConstraint >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLayout_SizeConstraint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLayoutItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLayoutItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLineEdit::ActionPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLineEdit_ActionPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLineEdit::EchoMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLineEdit_EchoMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLineEdit >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QLineEdit_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListView::Movement >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListView_Movement_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListView::Flow >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListView_Flow_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListView::ResizeMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListView_ResizeMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListView::LayoutMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListView_LayoutMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListView::ViewMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListView_ViewMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListView >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListWidgetItem::ItemType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListWidgetItem_ItemType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QListWidgetItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QListWidgetItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMainWindow::DockOption >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMainWindow_DockOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QMainWindow::DockOption> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QMainWindow_DockOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMainWindow >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMainWindow_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMdiArea::AreaOption >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMdiArea_AreaOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QMdiArea::AreaOption> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QMdiArea_AreaOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMdiArea::WindowOrder >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMdiArea_WindowOrder_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMdiArea::ViewMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMdiArea_ViewMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMdiArea >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMdiArea_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMdiSubWindow::SubWindowOption >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMdiSubWindow_SubWindowOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QMdiSubWindow::SubWindowOption> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QMdiSubWindow_SubWindowOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMdiSubWindow >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMdiSubWindow_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMenu >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMenu_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMenuBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMenuBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMessageBox::Option >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMessageBox_Option_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QMessageBox::Option> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QMessageBox_Option_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMessageBox::Icon >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMessageBox_Icon_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMessageBox::ButtonRole >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMessageBox_ButtonRole_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMessageBox::StandardButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMessageBox_StandardButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QMessageBox::StandardButton> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QMessageBox_StandardButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMessageBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QMessageBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPanGesture >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QPanGesture_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPinchGesture::ChangeFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QPinchGesture_ChangeFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QPinchGesture::ChangeFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QPinchGesture_ChangeFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPinchGesture >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QPinchGesture_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPlainTextDocumentLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QPlainTextDocumentLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPlainTextEdit::LineWrapMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QPlainTextEdit_LineWrapMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPlainTextEdit >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QPlainTextEdit_IDX]); }
template<> inline PyTypeObject *SbkType< ::QProgressBar::Direction >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QProgressBar_Direction_IDX]); }
template<> inline PyTypeObject *SbkType< ::QProgressBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QProgressBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QProgressDialog >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QProgressDialog_IDX]); }
template<> inline PyTypeObject *SbkType< ::QProxyStyle >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QProxyStyle_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPushButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QPushButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRadioButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QRadioButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRhiWidget::Api >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QRhiWidget_Api_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRhiWidget::TextureFormat >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QRhiWidget_TextureFormat_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRhiWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QRhiWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRubberBand::Shape >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QRubberBand_Shape_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRubberBand >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QRubberBand_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScrollArea >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScrollArea_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScrollBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScrollBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScroller::State >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScroller_State_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScroller::ScrollerGestureType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScroller_ScrollerGestureType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScroller::Input >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScroller_Input_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScroller >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScroller_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScrollerProperties::OvershootPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScrollerProperties_OvershootPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScrollerProperties::FrameRates >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScrollerProperties_FrameRates_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScrollerProperties::ScrollMetric >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScrollerProperties_ScrollMetric_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScrollerProperties >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QScrollerProperties_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSizeGrip >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSizeGrip_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSizePolicy::PolicyFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSizePolicy_PolicyFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSizePolicy::Policy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSizePolicy_Policy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSizePolicy::ControlType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSizePolicy_ControlType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QSizePolicy::ControlType> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QSizePolicy_ControlType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSizePolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSizePolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSlider::TickPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSlider_TickPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSlider >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSlider_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSpacerItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSpacerItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSpinBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSpinBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSplashScreen >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSplashScreen_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSplitter >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSplitter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSplitterHandle >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSplitterHandle_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStackedLayout::StackingMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStackedLayout_StackingMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStackedLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStackedLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStackedWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStackedWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStatusBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStatusBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::StateFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_StateFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyle::StateFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyle_StateFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::PrimitiveElement >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_PrimitiveElement_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::ControlElement >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_ControlElement_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::SubElement >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_SubElement_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::ComplexControl >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_ComplexControl_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::SubControl >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_SubControl_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyle::SubControl> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyle_SubControl_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::PixelMetric >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_PixelMetric_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::ContentsType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_ContentsType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::RequestSoftwareInputPanel >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_RequestSoftwareInputPanel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::StyleHint >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_StyleHint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle::StandardPixmap >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_StandardPixmap_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyle >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyle_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleFactory >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleFactory_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturn::HintReturnType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturn_HintReturnType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturn::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturn_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturn::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturn_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturn >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturn_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturnMask::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturnMask_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturnMask::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturnMask_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturnMask >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturnMask_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturnVariant::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturnVariant_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturnVariant::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturnVariant_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleHintReturnVariant >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleHintReturnVariant_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOption::OptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOption_OptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOption::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOption_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOption::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOption_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOption >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionButton::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionButton_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionButton::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionButton_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionButton::ButtonFeature >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionButton_ButtonFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyleOptionButton::ButtonFeature> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyleOptionButton_ButtonFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionComboBox::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionComboBox_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionComboBox::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionComboBox_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionComboBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionComboBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionComplex::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionComplex_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionComplex::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionComplex_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionComplex >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionComplex_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionDockWidget::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionDockWidget_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionDockWidget::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionDockWidget_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionDockWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionDockWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionFocusRect::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionFocusRect_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionFocusRect::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionFocusRect_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionFocusRect >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionFocusRect_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionFrame::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionFrame_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionFrame::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionFrame_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionFrame::FrameFeature >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionFrame_FrameFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyleOptionFrame::FrameFeature> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyleOptionFrame_FrameFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionFrame >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionFrame_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionGraphicsItem::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionGraphicsItem_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionGraphicsItem::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionGraphicsItem_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionGraphicsItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionGraphicsItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionGroupBox::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionGroupBox_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionGroupBox::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionGroupBox_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionGroupBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionGroupBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeader::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeader_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeader::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeader_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeader::SectionPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeader_SectionPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeader::SelectedPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeader_SelectedPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeader::SortIndicator >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeader_SortIndicator_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeader >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeader_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeaderV2::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeaderV2_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeaderV2::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeaderV2_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionHeaderV2 >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionHeaderV2_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionMenuItem::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionMenuItem_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionMenuItem::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionMenuItem_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionMenuItem::MenuItemType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionMenuItem_MenuItemType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionMenuItem::CheckType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionMenuItem_CheckType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionMenuItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionMenuItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionProgressBar::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionProgressBar_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionProgressBar::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionProgressBar_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionProgressBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionProgressBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionRubberBand::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionRubberBand_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionRubberBand::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionRubberBand_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionRubberBand >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionRubberBand_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSizeGrip::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSizeGrip_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSizeGrip::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSizeGrip_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSizeGrip >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSizeGrip_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSlider::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSlider_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSlider::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSlider_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSlider >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSlider_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSpinBox::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSpinBox_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSpinBox::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSpinBox_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionSpinBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionSpinBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTab::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTab_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTab::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTab_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTab::TabPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTab_TabPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTab::SelectedPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTab_SelectedPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTab::CornerWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTab_CornerWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyleOptionTab::CornerWidget> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyleOptionTab_CornerWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTab::TabFeature >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTab_TabFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyleOptionTab::TabFeature> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyleOptionTab_TabFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTab >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTab_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTabBarBase::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTabBarBase_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTabBarBase::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTabBarBase_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTabBarBase >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTabBarBase_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTabWidgetFrame::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTabWidgetFrame_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTabWidgetFrame::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTabWidgetFrame_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTabWidgetFrame >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTabWidgetFrame_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTitleBar::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTitleBar_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTitleBar::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTitleBar_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionTitleBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionTitleBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBar::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBar_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBar::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBar_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBar::ToolBarPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBar_ToolBarPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBar::ToolBarFeature >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBar_ToolBarFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyleOptionToolBar::ToolBarFeature> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyleOptionToolBar_ToolBarFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBox::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBox_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBox::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBox_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBox::TabPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBox_TabPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBox::SelectedPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBox_SelectedPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolButton::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolButton_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolButton::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolButton_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolButton::ToolButtonFeature >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolButton_ToolButtonFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyleOptionToolButton::ToolButtonFeature> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyleOptionToolButton_ToolButtonFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionToolButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionToolButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionViewItem::StyleOptionType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionViewItem_StyleOptionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionViewItem::StyleOptionVersion >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionViewItem_StyleOptionVersion_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionViewItem::Position >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionViewItem_Position_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionViewItem::ViewItemFeature >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionViewItem_ViewItemFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QStyleOptionViewItem::ViewItemFeature> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QStyleOptionViewItem_ViewItemFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionViewItem::ViewItemPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionViewItem_ViewItemPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyleOptionViewItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyleOptionViewItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStylePainter >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStylePainter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStyledItemDelegate >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QStyledItemDelegate_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSwipeGesture::SwipeDirection >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSwipeGesture_SwipeDirection_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSwipeGesture >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSwipeGesture_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSystemTrayIcon::ActivationReason >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSystemTrayIcon_ActivationReason_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSystemTrayIcon::MessageIcon >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSystemTrayIcon_MessageIcon_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSystemTrayIcon >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QSystemTrayIcon_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTabBar::Shape >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTabBar_Shape_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTabBar::ButtonPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTabBar_ButtonPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTabBar::SelectionBehavior >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTabBar_SelectionBehavior_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTabBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTabBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTabWidget::TabPosition >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTabWidget_TabPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTabWidget::TabShape >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTabWidget_TabShape_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTabWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTabWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTableView >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTableView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTableWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTableWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTableWidgetItem::ItemType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTableWidgetItem_ItemType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTableWidgetItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTableWidgetItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTableWidgetSelectionRange >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTableWidgetSelectionRange_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTapAndHoldGesture >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTapAndHoldGesture_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTapGesture >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTapGesture_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextBrowser >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTextBrowser_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextEdit::LineWrapMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTextEdit_LineWrapMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextEdit::AutoFormattingFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTextEdit_AutoFormattingFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QTextEdit::AutoFormattingFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QTextEdit_AutoFormattingFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextEdit >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTextEdit_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextEdit::ExtraSelection >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTextEdit_ExtraSelection_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTileRules >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTileRules_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTimeEdit >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTimeEdit_IDX]); }
template<> inline PyTypeObject *SbkType< ::QToolBar >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QToolBar_IDX]); }
template<> inline PyTypeObject *SbkType< ::QToolBox >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QToolBox_IDX]); }
template<> inline PyTypeObject *SbkType< ::QToolButton::ToolButtonPopupMode >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QToolButton_ToolButtonPopupMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QToolButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QToolButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QToolTip >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QToolTip_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTreeView >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTreeView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTreeWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTreeWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTreeWidgetItem::ItemType >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTreeWidgetItem_ItemType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTreeWidgetItem::ChildIndicatorPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTreeWidgetItem_ChildIndicatorPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTreeWidgetItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTreeWidgetItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTreeWidgetItemIterator::IteratorFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTreeWidgetItemIterator_IteratorFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QTreeWidgetItemIterator::IteratorFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QTreeWidgetItemIterator_IteratorFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTreeWidgetItemIterator >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QTreeWidgetItemIterator_IDX]); }
template<> inline PyTypeObject *SbkType< ::QUndoView >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QUndoView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVBoxLayout >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QVBoxLayout_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWhatsThis >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWhatsThis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWidget::RenderFlag >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWidget_RenderFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QWidget::RenderFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QWidget_RenderFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWidget >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWidgetAction >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWidgetAction_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWidgetItem >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWidgetItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWizard::WizardButton >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWizard_WizardButton_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWizard::WizardPixmap >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWizard_WizardPixmap_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWizard::WizardStyle >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWizard_WizardStyle_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWizard::WizardOption >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWizard_WizardOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QWizard::WizardOption> >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QFlags_QWizard_WizardOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWizard >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWizard_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWizardPage >() { return Shiboken::Module::get(SbkPySide6_QtWidgetsTypeStructs[SBK_QWizardPage_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTWIDGETS_PYTHON_H

