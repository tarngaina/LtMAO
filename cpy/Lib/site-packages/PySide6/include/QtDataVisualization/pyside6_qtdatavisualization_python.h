// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTDATAVISUALIZATION_PYTHON_H
#define SBK_QTDATAVISUALIZATION_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtgui_python.h>
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QtDataVisualization/q3dcamera.h>
#include <QtDataVisualization/q3dtheme.h>
#include <QtDataVisualization/qabstract3daxis.h>
#include <QtDataVisualization/qabstract3dgraph.h>
#include <QtDataVisualization/qabstract3dinputhandler.h>
#include <QtDataVisualization/qabstract3dseries.h>
#include <QtDataVisualization/qabstractdataproxy.h>
#include <QtDataVisualization/qitemmodelbardataproxy.h>
#include <QtDataVisualization/qitemmodelsurfacedataproxy.h>
#include <QtDataVisualization/qsurface3dseries.h>

QT_BEGIN_NAMESPACE
class Q3DBars;
class Q3DInputHandler;
class Q3DLight;
class Q3DObject;
class Q3DScatter;
class Q3DScene;
class Q3DSurface;
class QBar3DSeries;
class QBarDataItem;
class QBarDataProxy;
class QCategory3DAxis;
class QCustom3DItem;
class QCustom3DLabel;
class QCustom3DVolume;
class QHeightMapSurfaceDataProxy;
class QItemModelScatterDataProxy;
class QLogValue3DAxisFormatter;
class QScatter3DSeries;
class QScatterDataItem;
class QScatterDataProxy;
class QSurfaceDataItem;
class QSurfaceDataProxy;
class QTouch3DInputHandler;
class QValue3DAxis;
class QValue3DAxisFormatter;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_Q3DBARS_IDX                                          = 0,
    SBK_Q3DCAMERA_CAMERAPRESET_IDX                           = 4,
    SBK_Q3DCAMERA_IDX                                        = 2,
    SBK_Q3DINPUTHANDLER_IDX                                  = 6,
    SBK_Q3DLIGHT_IDX                                         = 8,
    SBK_Q3DOBJECT_IDX                                        = 10,
    SBK_Q3DSCATTER_IDX                                       = 12,
    SBK_Q3DSCENE_IDX                                         = 14,
    SBK_Q3DSURFACE_IDX                                       = 16,
    SBK_Q3DTHEME_COLORSTYLE_IDX                              = 20,
    SBK_Q3DTHEME_THEME_IDX                                   = 22,
    SBK_Q3DTHEME_IDX                                         = 18,
    SBK_QABSTRACT3DAXIS_AXISORIENTATION_IDX                  = 26,
    SBK_QABSTRACT3DAXIS_AXISTYPE_IDX                         = 28,
    SBK_QABSTRACT3DAXIS_IDX                                  = 24,
    SBK_QABSTRACT3DGRAPH_SELECTIONFLAG_IDX                   = 36,
    SBK_QFLAGS_QABSTRACT3DGRAPH_SELECTIONFLAG_IDX            = 70,
    SBK_QABSTRACT3DGRAPH_SHADOWQUALITY_IDX                   = 38,
    SBK_QABSTRACT3DGRAPH_ELEMENTTYPE_IDX                     = 32,
    SBK_QABSTRACT3DGRAPH_OPTIMIZATIONHINT_IDX                = 34,
    SBK_QFLAGS_QABSTRACT3DGRAPH_OPTIMIZATIONHINT_IDX         = 68,
    SBK_QABSTRACT3DGRAPH_IDX                                 = 30,
    SBK_QABSTRACT3DINPUTHANDLER_INPUTVIEW_IDX                = 42,
    SBK_QABSTRACT3DINPUTHANDLER_IDX                          = 40,
    SBK_QABSTRACT3DSERIES_SERIESTYPE_IDX                     = 48,
    SBK_QABSTRACT3DSERIES_MESH_IDX                           = 46,
    SBK_QABSTRACT3DSERIES_IDX                                = 44,
    SBK_QABSTRACTDATAPROXY_DATATYPE_IDX                      = 52,
    SBK_QABSTRACTDATAPROXY_IDX                               = 50,
    SBK_QBAR3DSERIES_IDX                                     = 54,
    SBK_QBARDATAITEM_IDX                                     = 56,
    SBK_QBARDATAPROXY_IDX                                    = 58,
    SBK_QCATEGORY3DAXIS_IDX                                  = 60,
    SBK_QCUSTOM3DITEM_IDX                                    = 62,
    SBK_QCUSTOM3DLABEL_IDX                                   = 64,
    SBK_QCUSTOM3DVOLUME_IDX                                  = 66,
    SBK_QHEIGHTMAPSURFACEDATAPROXY_IDX                       = 74,
    SBK_QITEMMODELBARDATAPROXY_MULTIMATCHBEHAVIOR_IDX        = 78,
    SBK_QITEMMODELBARDATAPROXY_IDX                           = 76,
    SBK_QITEMMODELSCATTERDATAPROXY_IDX                       = 80,
    SBK_QITEMMODELSURFACEDATAPROXY_MULTIMATCHBEHAVIOR_IDX    = 84,
    SBK_QITEMMODELSURFACEDATAPROXY_IDX                       = 82,
    SBK_QLOGVALUE3DAXISFORMATTER_IDX                         = 86,
    SBK_QSCATTER3DSERIES_IDX                                 = 88,
    SBK_QSCATTERDATAITEM_IDX                                 = 90,
    SBK_QSCATTERDATAPROXY_IDX                                = 92,
    SBK_QSURFACE3DSERIES_DRAWFLAG_IDX                        = 96,
    SBK_QFLAGS_QSURFACE3DSERIES_DRAWFLAG_IDX                 = 72,
    SBK_QSURFACE3DSERIES_IDX                                 = 94,
    SBK_QSURFACEDATAITEM_IDX                                 = 98,
    SBK_QSURFACEDATAPROXY_IDX                                = 100,
    SBK_QTOUCH3DINPUTHANDLER_IDX                             = 102,
    SBK_QVALUE3DAXIS_IDX                                     = 104,
    SBK_QVALUE3DAXISFORMATTER_IDX                            = 106,
    SBK_QTDATAVISUALIZATION_IDX_COUNT                        = 108,
};

// Type indices
enum : int {
    SBK_Q3DBars_IDX                                          = 0,
    SBK_Q3DCamera_CameraPreset_IDX                           = 2,
    SBK_Q3DCamera_IDX                                        = 1,
    SBK_Q3DInputHandler_IDX                                  = 3,
    SBK_Q3DLight_IDX                                         = 4,
    SBK_Q3DObject_IDX                                        = 5,
    SBK_Q3DScatter_IDX                                       = 6,
    SBK_Q3DScene_IDX                                         = 7,
    SBK_Q3DSurface_IDX                                       = 8,
    SBK_Q3DTheme_ColorStyle_IDX                              = 10,
    SBK_Q3DTheme_Theme_IDX                                   = 11,
    SBK_Q3DTheme_IDX                                         = 9,
    SBK_QAbstract3DAxis_AxisOrientation_IDX                  = 13,
    SBK_QAbstract3DAxis_AxisType_IDX                         = 14,
    SBK_QAbstract3DAxis_IDX                                  = 12,
    SBK_QAbstract3DGraph_SelectionFlag_IDX                   = 18,
    SBK_QFlags_QAbstract3DGraph_SelectionFlag_IDX            = 35,
    SBK_QAbstract3DGraph_ShadowQuality_IDX                   = 19,
    SBK_QAbstract3DGraph_ElementType_IDX                     = 16,
    SBK_QAbstract3DGraph_OptimizationHint_IDX                = 17,
    SBK_QFlags_QAbstract3DGraph_OptimizationHint_IDX         = 34,
    SBK_QAbstract3DGraph_IDX                                 = 15,
    SBK_QAbstract3DInputHandler_InputView_IDX                = 21,
    SBK_QAbstract3DInputHandler_IDX                          = 20,
    SBK_QAbstract3DSeries_SeriesType_IDX                     = 24,
    SBK_QAbstract3DSeries_Mesh_IDX                           = 23,
    SBK_QAbstract3DSeries_IDX                                = 22,
    SBK_QAbstractDataProxy_DataType_IDX                      = 26,
    SBK_QAbstractDataProxy_IDX                               = 25,
    SBK_QBar3DSeries_IDX                                     = 27,
    SBK_QBarDataItem_IDX                                     = 28,
    SBK_QBarDataProxy_IDX                                    = 29,
    SBK_QCategory3DAxis_IDX                                  = 30,
    SBK_QCustom3DItem_IDX                                    = 31,
    SBK_QCustom3DLabel_IDX                                   = 32,
    SBK_QCustom3DVolume_IDX                                  = 33,
    SBK_QHeightMapSurfaceDataProxy_IDX                       = 37,
    SBK_QItemModelBarDataProxy_MultiMatchBehavior_IDX        = 39,
    SBK_QItemModelBarDataProxy_IDX                           = 38,
    SBK_QItemModelScatterDataProxy_IDX                       = 40,
    SBK_QItemModelSurfaceDataProxy_MultiMatchBehavior_IDX    = 42,
    SBK_QItemModelSurfaceDataProxy_IDX                       = 41,
    SBK_QLogValue3DAxisFormatter_IDX                         = 43,
    SBK_QScatter3DSeries_IDX                                 = 44,
    SBK_QScatterDataItem_IDX                                 = 45,
    SBK_QScatterDataProxy_IDX                                = 46,
    SBK_QSurface3DSeries_DrawFlag_IDX                        = 48,
    SBK_QFlags_QSurface3DSeries_DrawFlag_IDX                 = 36,
    SBK_QSurface3DSeries_IDX                                 = 47,
    SBK_QSurfaceDataItem_IDX                                 = 49,
    SBK_QSurfaceDataProxy_IDX                                = 50,
    SBK_QTouch3DInputHandler_IDX                             = 51,
    SBK_QValue3DAxis_IDX                                     = 52,
    SBK_QValue3DAxisFormatter_IDX                            = 53,
    SBK_QtDataVisualization_IDX_COUNT                        = 54,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtDataVisualizationTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtDataVisualizationTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtDataVisualizationModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtDataVisualizationTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QBARDATAARRAY_IDX                                    = 0,
    SBK_QSURFACEDATAARRAY_IDX                                = 2,
    SBK_QTDATAVISUALIZATION_QLIST_INT_IDX                    = 4, // QList<int>
    SBK_QTDATAVISUALIZATION_QLIST_QCUSTOM3DITEMPTR_IDX       = 6, // QList<QCustom3DItem*>
    SBK_QTDATAVISUALIZATION_QLIST_QABSTRACT3DINPUTHANDLERPTR_IDX = 8, // QList<QAbstract3DInputHandler*>
    SBK_QTDATAVISUALIZATION_QLIST_Q3DTHEMEPTR_IDX            = 10, // QList<Q3DTheme*>
    SBK_QTDATAVISUALIZATION_QLIST_QVALUE3DAXISPTR_IDX        = 12, // QList<QValue3DAxis*>
    SBK_QTDATAVISUALIZATION_QLIST_QSURFACE3DSERIESPTR_IDX    = 14, // QList<QSurface3DSeries*>
    SBK_QTDATAVISUALIZATION_QLIST_QSCATTER3DSERIESPTR_IDX    = 16, // QList<QScatter3DSeries*>
    SBK_QTDATAVISUALIZATION_QLIST_QABSTRACT3DAXISPTR_IDX     = 18, // QList<QAbstract3DAxis*>
    SBK_QTDATAVISUALIZATION_QLIST_QBAR3DSERIESPTR_IDX        = 20, // QList<QBar3DSeries*>
    SBK_QTDATAVISUALIZATION_QLIST_QOBJECTPTR_IDX             = 22, // QList<QObject*>
    SBK_QTDATAVISUALIZATION_QLIST_QBYTEARRAY_IDX             = 24, // QList<QByteArray>
    SBK_QTDATAVISUALIZATION_QLIST_FLOAT_IDX                  = 26, // QList<float>
    SBK_QTDATAVISUALIZATION_QLIST_UCHAR_IDX                  = 28, // QList<uchar>
    SBK_QTDATAVISUALIZATION_QLIST_UNSIGNEDINT_IDX            = 30, // QList<unsigned int>
    SBK_QTDATAVISUALIZATION_QLIST_QIMAGEPTR_IDX              = 32, // QList<QImage*>
    SBK_QTDATAVISUALIZATION_QLIST_QSURFACEDATAITEM_IDX       = 34, // QList<QSurfaceDataItem>
    SBK_QTDATAVISUALIZATION_QLIST_QSCATTERDATAITEM_IDX       = 36, // QList<QScatterDataItem>
    SBK_QTDATAVISUALIZATION_QLIST_QBARDATAITEM_IDX           = 38, // QList<QBarDataItem>
    SBK_QTDATAVISUALIZATION_QLIST_QCOLOR_IDX                 = 40, // QList<QColor>
    SBK_QTDATAVISUALIZATION_QLIST_QLINEARGRADIENT_IDX        = 42, // QList<QLinearGradient>
    SBK_QTDATAVISUALIZATION_QLIST_QVARIANT_IDX               = 44, // QList<QVariant>
    SBK_QTDATAVISUALIZATION_QLIST_QSTRING_IDX                = 46, // QList<QString>
    SBK_QTDATAVISUALIZATION_QMAP_QSTRING_QVARIANT_IDX        = 48, // QMap<QString,QVariant>
    SBK_QTDATAVISUALIZATION_CONVERTERS_IDX_COUNT             = 50,
};

// Converter indices
enum : int {
    SBK_QBarDataArray_IDX                                    = 0,
    SBK_QSurfaceDataArray_IDX                                = 1,
    SBK_QtDataVisualization_QList_int_IDX                    = 2, // QList<int>
    SBK_QtDataVisualization_QList_QCustom3DItemPTR_IDX       = 3, // QList<QCustom3DItem*>
    SBK_QtDataVisualization_QList_QAbstract3DInputHandlerPTR_IDX = 4, // QList<QAbstract3DInputHandler*>
    SBK_QtDataVisualization_QList_Q3DThemePTR_IDX            = 5, // QList<Q3DTheme*>
    SBK_QtDataVisualization_QList_QValue3DAxisPTR_IDX        = 6, // QList<QValue3DAxis*>
    SBK_QtDataVisualization_QList_QSurface3DSeriesPTR_IDX    = 7, // QList<QSurface3DSeries*>
    SBK_QtDataVisualization_QList_QScatter3DSeriesPTR_IDX    = 8, // QList<QScatter3DSeries*>
    SBK_QtDataVisualization_QList_QAbstract3DAxisPTR_IDX     = 9, // QList<QAbstract3DAxis*>
    SBK_QtDataVisualization_QList_QBar3DSeriesPTR_IDX        = 10, // QList<QBar3DSeries*>
    SBK_QtDataVisualization_QList_QObjectPTR_IDX             = 11, // QList<QObject*>
    SBK_QtDataVisualization_QList_QByteArray_IDX             = 12, // QList<QByteArray>
    SBK_QtDataVisualization_QList_float_IDX                  = 13, // QList<float>
    SBK_QtDataVisualization_QList_uchar_IDX                  = 14, // QList<uchar>
    SBK_QtDataVisualization_QList_unsignedint_IDX            = 15, // QList<unsigned int>
    SBK_QtDataVisualization_QList_QImagePTR_IDX              = 16, // QList<QImage*>
    SBK_QtDataVisualization_QList_QSurfaceDataItem_IDX       = 17, // QList<QSurfaceDataItem>
    SBK_QtDataVisualization_QList_QScatterDataItem_IDX       = 18, // QList<QScatterDataItem>
    SBK_QtDataVisualization_QList_QBarDataItem_IDX           = 19, // QList<QBarDataItem>
    SBK_QtDataVisualization_QList_QColor_IDX                 = 20, // QList<QColor>
    SBK_QtDataVisualization_QList_QLinearGradient_IDX        = 21, // QList<QLinearGradient>
    SBK_QtDataVisualization_QList_QVariant_IDX               = 22, // QList<QVariant>
    SBK_QtDataVisualization_QList_QString_IDX                = 23, // QList<QString>
    SBK_QtDataVisualization_QMap_QString_QVariant_IDX        = 24, // QMap<QString,QVariant>
    SBK_QtDataVisualization_CONVERTERS_IDX_COUNT             = 25,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::Q3DBars >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DBars_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DCamera::CameraPreset >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DCamera_CameraPreset_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DCamera >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DCamera_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DInputHandler >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DInputHandler_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DLight >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DLight_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DObject >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DObject_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DScatter >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DScatter_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DScene >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DScene_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DSurface >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DSurface_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DTheme::ColorStyle >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DTheme_ColorStyle_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DTheme::Theme >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DTheme_Theme_IDX]); }
template<> inline PyTypeObject *SbkType< ::Q3DTheme >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_Q3DTheme_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DAxis::AxisOrientation >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DAxis_AxisOrientation_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DAxis::AxisType >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DAxis_AxisType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DAxis >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DGraph::SelectionFlag >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DGraph_SelectionFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QAbstract3DGraph::SelectionFlag> >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QFlags_QAbstract3DGraph_SelectionFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DGraph::ShadowQuality >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DGraph_ShadowQuality_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DGraph::ElementType >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DGraph_ElementType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DGraph::OptimizationHint >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DGraph_OptimizationHint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QAbstract3DGraph::OptimizationHint> >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QFlags_QAbstract3DGraph_OptimizationHint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DGraph >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DGraph_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DInputHandler::InputView >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DInputHandler_InputView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DInputHandler >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DInputHandler_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DSeries::SeriesType >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DSeries_SeriesType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DSeries::Mesh >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DSeries_Mesh_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstract3DSeries >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstract3DSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractDataProxy::DataType >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstractDataProxy_DataType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractDataProxy >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QAbstractDataProxy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBar3DSeries >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QBar3DSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBarDataItem >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QBarDataItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBarDataProxy >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QBarDataProxy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCategory3DAxis >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QCategory3DAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCustom3DItem >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QCustom3DItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCustom3DLabel >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QCustom3DLabel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCustom3DVolume >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QCustom3DVolume_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHeightMapSurfaceDataProxy >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QHeightMapSurfaceDataProxy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QItemModelBarDataProxy::MultiMatchBehavior >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QItemModelBarDataProxy_MultiMatchBehavior_IDX]); }
template<> inline PyTypeObject *SbkType< ::QItemModelBarDataProxy >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QItemModelBarDataProxy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QItemModelScatterDataProxy >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QItemModelScatterDataProxy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QItemModelSurfaceDataProxy::MultiMatchBehavior >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QItemModelSurfaceDataProxy_MultiMatchBehavior_IDX]); }
template<> inline PyTypeObject *SbkType< ::QItemModelSurfaceDataProxy >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QItemModelSurfaceDataProxy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLogValue3DAxisFormatter >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QLogValue3DAxisFormatter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScatter3DSeries >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QScatter3DSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScatterDataItem >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QScatterDataItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScatterDataProxy >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QScatterDataProxy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSurface3DSeries::DrawFlag >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QSurface3DSeries_DrawFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QSurface3DSeries::DrawFlag> >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QFlags_QSurface3DSeries_DrawFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSurface3DSeries >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QSurface3DSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSurfaceDataItem >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QSurfaceDataItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSurfaceDataProxy >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QSurfaceDataProxy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTouch3DInputHandler >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QTouch3DInputHandler_IDX]); }
template<> inline PyTypeObject *SbkType< ::QValue3DAxis >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QValue3DAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QValue3DAxisFormatter >() { return Shiboken::Module::get(SbkPySide6_QtDataVisualizationTypeStructs[SBK_QValue3DAxisFormatter_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTDATAVISUALIZATION_PYTHON_H

