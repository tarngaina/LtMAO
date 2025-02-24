// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTCHARTS_PYTHON_H
#define SBK_QTCHARTS_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtwidgets_python.h>
#include <pyside6_qtgui_python.h>
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QtCharts/qabstractaxis.h>
#include <QtCharts/qabstractbarseries.h>
#include <QtCharts/qabstractseries.h>
#include <QtCharts/qboxset.h>
#include <QtCharts/qcategoryaxis.h>
#include <QtCharts/qchart.h>
#include <QtCharts/qchartview.h>
#include <QtCharts/qlegend.h>
#include <QtCharts/qlegendmarker.h>
#include <QtCharts/qpieslice.h>
#include <QtCharts/qpolarchart.h>
#include <QtCharts/qscatterseries.h>
#include <QtCharts/qvalueaxis.h>
#include <QtCharts/qxyseries.h>
#include <pyside_numpy.h>

QT_BEGIN_NAMESPACE
class QAreaLegendMarker;
class QAreaSeries;
class QBarCategoryAxis;
class QBarLegendMarker;
class QBarModelMapper;
class QBarSeries;
class QBarSet;
class QBoxPlotLegendMarker;
class QBoxPlotModelMapper;
class QBoxPlotSeries;
class QCandlestickLegendMarker;
class QCandlestickModelMapper;
class QCandlestickSeries;
class QCandlestickSet;
class QColorAxis;
class QDateTimeAxis;
class QHBarModelMapper;
class QHBoxPlotModelMapper;
class QHCandlestickModelMapper;
class QHPieModelMapper;
class QHXYModelMapper;
class QHorizontalBarSeries;
class QHorizontalPercentBarSeries;
class QHorizontalStackedBarSeries;
class QLineSeries;
class QLogValueAxis;
class QPercentBarSeries;
class QPieLegendMarker;
class QPieModelMapper;
class QPieSeries;
class QSplineSeries;
class QStackedBarSeries;
class QVBarModelMapper;
class QVBoxPlotModelMapper;
class QVCandlestickModelMapper;
class QVPieModelMapper;
class QVXYModelMapper;
class QXYLegendMarker;
class QXYModelMapper;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QABSTRACTAXIS_AXISTYPE_IDX                           = 2,
    SBK_QABSTRACTAXIS_IDX                                    = 0,
    SBK_QABSTRACTBARSERIES_LABELSPOSITION_IDX                = 6,
    SBK_QABSTRACTBARSERIES_IDX                               = 4,
    SBK_QABSTRACTSERIES_SERIESTYPE_IDX                       = 10,
    SBK_QABSTRACTSERIES_IDX                                  = 8,
    SBK_QAREALEGENDMARKER_IDX                                = 12,
    SBK_QAREASERIES_IDX                                      = 14,
    SBK_QBARCATEGORYAXIS_IDX                                 = 16,
    SBK_QBARLEGENDMARKER_IDX                                 = 18,
    SBK_QBARMODELMAPPER_IDX                                  = 20,
    SBK_QBARSERIES_IDX                                       = 22,
    SBK_QBARSET_IDX                                          = 24,
    SBK_QBOXPLOTLEGENDMARKER_IDX                             = 26,
    SBK_QBOXPLOTMODELMAPPER_IDX                              = 28,
    SBK_QBOXPLOTSERIES_IDX                                   = 30,
    SBK_QBOXSET_VALUEPOSITIONS_IDX                           = 34,
    SBK_QBOXSET_IDX                                          = 32,
    SBK_QCANDLESTICKLEGENDMARKER_IDX                         = 36,
    SBK_QCANDLESTICKMODELMAPPER_IDX                          = 38,
    SBK_QCANDLESTICKSERIES_IDX                               = 40,
    SBK_QCANDLESTICKSET_IDX                                  = 42,
    SBK_QCATEGORYAXIS_AXISLABELSPOSITION_IDX                 = 46,
    SBK_QCATEGORYAXIS_IDX                                    = 44,
    SBK_QCHART_CHARTTYPE_IDX                                 = 54,
    SBK_QCHART_CHARTTHEME_IDX                                = 52,
    SBK_QCHART_ANIMATIONOPTION_IDX                           = 50,
    SBK_QFLAGS_QCHART_ANIMATIONOPTION_IDX                    = 64,
    SBK_QCHART_IDX                                           = 48,
    SBK_QCHARTVIEW_RUBBERBAND_IDX                            = 58,
    SBK_QFLAGS_QCHARTVIEW_RUBBERBAND_IDX                     = 66,
    SBK_QCHARTVIEW_IDX                                       = 56,
    SBK_QCOLORAXIS_IDX                                       = 60,
    SBK_QDATETIMEAXIS_IDX                                    = 62,
    SBK_QHBARMODELMAPPER_IDX                                 = 70,
    SBK_QHBOXPLOTMODELMAPPER_IDX                             = 72,
    SBK_QHCANDLESTICKMODELMAPPER_IDX                         = 74,
    SBK_QHPIEMODELMAPPER_IDX                                 = 76,
    SBK_QHXYMODELMAPPER_IDX                                  = 78,
    SBK_QHORIZONTALBARSERIES_IDX                             = 80,
    SBK_QHORIZONTALPERCENTBARSERIES_IDX                      = 82,
    SBK_QHORIZONTALSTACKEDBARSERIES_IDX                      = 84,
    SBK_QLEGEND_MARKERSHAPE_IDX                              = 88,
    SBK_QLEGEND_IDX                                          = 86,
    SBK_QLEGENDMARKER_LEGENDMARKERTYPE_IDX                   = 92,
    SBK_QLEGENDMARKER_IDX                                    = 90,
    SBK_QLINESERIES_IDX                                      = 94,
    SBK_QLOGVALUEAXIS_IDX                                    = 96,
    SBK_QPERCENTBARSERIES_IDX                                = 98,
    SBK_QPIELEGENDMARKER_IDX                                 = 100,
    SBK_QPIEMODELMAPPER_IDX                                  = 102,
    SBK_QPIESERIES_IDX                                       = 104,
    SBK_QPIESLICE_LABELPOSITION_IDX                          = 108,
    SBK_QPIESLICE_IDX                                        = 106,
    SBK_QPOLARCHART_POLARORIENTATION_IDX                     = 112,
    SBK_QFLAGS_QPOLARCHART_POLARORIENTATION_IDX              = 68,
    SBK_QPOLARCHART_IDX                                      = 110,
    SBK_QSCATTERSERIES_MARKERSHAPE_IDX                       = 116,
    SBK_QSCATTERSERIES_IDX                                   = 114,
    SBK_QSPLINESERIES_IDX                                    = 118,
    SBK_QSTACKEDBARSERIES_IDX                                = 120,
    SBK_QVBARMODELMAPPER_IDX                                 = 122,
    SBK_QVBOXPLOTMODELMAPPER_IDX                             = 124,
    SBK_QVCANDLESTICKMODELMAPPER_IDX                         = 126,
    SBK_QVPIEMODELMAPPER_IDX                                 = 128,
    SBK_QVXYMODELMAPPER_IDX                                  = 130,
    SBK_QVALUEAXIS_TICKTYPE_IDX                              = 134,
    SBK_QVALUEAXIS_IDX                                       = 132,
    SBK_QXYLEGENDMARKER_IDX                                  = 136,
    SBK_QXYMODELMAPPER_IDX                                   = 138,
    SBK_QXYSERIES_POINTCONFIGURATION_IDX                     = 142,
    SBK_QXYSERIES_IDX                                        = 140,
    SBK_QTCHARTS_IDX_COUNT                                   = 144,
};

// Type indices
enum : int {
    SBK_QAbstractAxis_AxisType_IDX                           = 1,
    SBK_QAbstractAxis_IDX                                    = 0,
    SBK_QAbstractBarSeries_LabelsPosition_IDX                = 3,
    SBK_QAbstractBarSeries_IDX                               = 2,
    SBK_QAbstractSeries_SeriesType_IDX                       = 5,
    SBK_QAbstractSeries_IDX                                  = 4,
    SBK_QAreaLegendMarker_IDX                                = 6,
    SBK_QAreaSeries_IDX                                      = 7,
    SBK_QBarCategoryAxis_IDX                                 = 8,
    SBK_QBarLegendMarker_IDX                                 = 9,
    SBK_QBarModelMapper_IDX                                  = 10,
    SBK_QBarSeries_IDX                                       = 11,
    SBK_QBarSet_IDX                                          = 12,
    SBK_QBoxPlotLegendMarker_IDX                             = 13,
    SBK_QBoxPlotModelMapper_IDX                              = 14,
    SBK_QBoxPlotSeries_IDX                                   = 15,
    SBK_QBoxSet_ValuePositions_IDX                           = 17,
    SBK_QBoxSet_IDX                                          = 16,
    SBK_QCandlestickLegendMarker_IDX                         = 18,
    SBK_QCandlestickModelMapper_IDX                          = 19,
    SBK_QCandlestickSeries_IDX                               = 20,
    SBK_QCandlestickSet_IDX                                  = 21,
    SBK_QCategoryAxis_AxisLabelsPosition_IDX                 = 23,
    SBK_QCategoryAxis_IDX                                    = 22,
    SBK_QChart_ChartType_IDX                                 = 27,
    SBK_QChart_ChartTheme_IDX                                = 26,
    SBK_QChart_AnimationOption_IDX                           = 25,
    SBK_QFlags_QChart_AnimationOption_IDX                    = 32,
    SBK_QChart_IDX                                           = 24,
    SBK_QChartView_RubberBand_IDX                            = 29,
    SBK_QFlags_QChartView_RubberBand_IDX                     = 33,
    SBK_QChartView_IDX                                       = 28,
    SBK_QColorAxis_IDX                                       = 30,
    SBK_QDateTimeAxis_IDX                                    = 31,
    SBK_QHBarModelMapper_IDX                                 = 35,
    SBK_QHBoxPlotModelMapper_IDX                             = 36,
    SBK_QHCandlestickModelMapper_IDX                         = 37,
    SBK_QHPieModelMapper_IDX                                 = 38,
    SBK_QHXYModelMapper_IDX                                  = 39,
    SBK_QHorizontalBarSeries_IDX                             = 40,
    SBK_QHorizontalPercentBarSeries_IDX                      = 41,
    SBK_QHorizontalStackedBarSeries_IDX                      = 42,
    SBK_QLegend_MarkerShape_IDX                              = 44,
    SBK_QLegend_IDX                                          = 43,
    SBK_QLegendMarker_LegendMarkerType_IDX                   = 46,
    SBK_QLegendMarker_IDX                                    = 45,
    SBK_QLineSeries_IDX                                      = 47,
    SBK_QLogValueAxis_IDX                                    = 48,
    SBK_QPercentBarSeries_IDX                                = 49,
    SBK_QPieLegendMarker_IDX                                 = 50,
    SBK_QPieModelMapper_IDX                                  = 51,
    SBK_QPieSeries_IDX                                       = 52,
    SBK_QPieSlice_LabelPosition_IDX                          = 54,
    SBK_QPieSlice_IDX                                        = 53,
    SBK_QPolarChart_PolarOrientation_IDX                     = 56,
    SBK_QFlags_QPolarChart_PolarOrientation_IDX              = 34,
    SBK_QPolarChart_IDX                                      = 55,
    SBK_QScatterSeries_MarkerShape_IDX                       = 58,
    SBK_QScatterSeries_IDX                                   = 57,
    SBK_QSplineSeries_IDX                                    = 59,
    SBK_QStackedBarSeries_IDX                                = 60,
    SBK_QVBarModelMapper_IDX                                 = 61,
    SBK_QVBoxPlotModelMapper_IDX                             = 62,
    SBK_QVCandlestickModelMapper_IDX                         = 63,
    SBK_QVPieModelMapper_IDX                                 = 64,
    SBK_QVXYModelMapper_IDX                                  = 65,
    SBK_QValueAxis_TickType_IDX                              = 67,
    SBK_QValueAxis_IDX                                       = 66,
    SBK_QXYLegendMarker_IDX                                  = 68,
    SBK_QXYModelMapper_IDX                                   = 69,
    SBK_QXYSeries_PointConfiguration_IDX                     = 71,
    SBK_QXYSeries_IDX                                        = 70,
    SBK_QtCharts_IDX_COUNT                                   = 72,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtChartsTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtChartsTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtChartsModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtChartsTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTCHARTS_QLIST_INT_IDX                               = 0, // QList<int>
    SBK_QTCHARTS_QLIST_QOBJECTPTR_IDX                        = 2, // QList<QObject*>
    SBK_QTCHARTS_QLIST_QBYTEARRAY_IDX                        = 4, // QList<QByteArray>
    SBK_QTCHARTS_QLIST_QACTIONPTR_IDX                        = 6, // QList<QAction*>
    SBK_QTCHARTS_QLIST_QLEGENDMARKERPTR_IDX                  = 8, // QList<QLegendMarker*>
    SBK_QTCHARTS_QLIST_QGRAPHICSITEMPTR_IDX                  = 10, // QList<QGraphicsItem*>
    SBK_QTCHARTS_QLIST_QRECTF_IDX                            = 12, // QList<QRectF>
    SBK_QTCHARTS_QLIST_QABSTRACTAXISPTR_IDX                  = 14, // QList<QAbstractAxis*>
    SBK_QTCHARTS_QLIST_QABSTRACTSERIESPTR_IDX                = 16, // QList<QAbstractSeries*>
    SBK_QTCHARTS_QLIST_QREAL_IDX                             = 18, // QList<qreal>
    SBK_QTCHARTS_QLIST_QPOINTF_IDX                           = 20, // QList<QPointF>
    SBK_QTCHARTS_STD_PAIR_QREAL_QREAL_IDX                    = 22, // std::pair<qreal,qreal>
    SBK_QTCHARTS_QHASH_QXYSERIES_POINTCONFIGURATION_QVARIANT_IDX = 24, // QHash<QXYSeries::PointConfiguration,QVariant>
    SBK_QTCHARTS_QHASH_INT_QHASH_QXYSERIES_POINTCONFIGURATION_QVARIANT_IDX = 26, // QHash<int,QHash<QXYSeries::PointConfiguration,QVariant>>
    SBK_QTCHARTS_QLIST_QPIESLICEPTR_IDX                      = 28, // QList<QPieSlice*>
    SBK_QTCHARTS_QLIST_QCANDLESTICKSETPTR_IDX                = 30, // QList<QCandlestickSet*>
    SBK_QTCHARTS_QLIST_QBOXSETPTR_IDX                        = 32, // QList<QBoxSet*>
    SBK_QTCHARTS_QLIST_QBARSETPTR_IDX                        = 34, // QList<QBarSet*>
    SBK_QTCHARTS_QLIST_QVARIANT_IDX                          = 36, // QList<QVariant>
    SBK_QTCHARTS_QLIST_QSTRING_IDX                           = 38, // QList<QString>
    SBK_QTCHARTS_QMAP_QSTRING_QVARIANT_IDX                   = 40, // QMap<QString,QVariant>
    SBK_QTCHARTS_CONVERTERS_IDX_COUNT                        = 42,
};

// Converter indices
enum : int {
    SBK_QtCharts_QList_int_IDX                               = 0, // QList<int>
    SBK_QtCharts_QList_QObjectPTR_IDX                        = 1, // QList<QObject*>
    SBK_QtCharts_QList_QByteArray_IDX                        = 2, // QList<QByteArray>
    SBK_QtCharts_QList_QActionPTR_IDX                        = 3, // QList<QAction*>
    SBK_QtCharts_QList_QLegendMarkerPTR_IDX                  = 4, // QList<QLegendMarker*>
    SBK_QtCharts_QList_QGraphicsItemPTR_IDX                  = 5, // QList<QGraphicsItem*>
    SBK_QtCharts_QList_QRectF_IDX                            = 6, // QList<QRectF>
    SBK_QtCharts_QList_QAbstractAxisPTR_IDX                  = 7, // QList<QAbstractAxis*>
    SBK_QtCharts_QList_QAbstractSeriesPTR_IDX                = 8, // QList<QAbstractSeries*>
    SBK_QtCharts_QList_qreal_IDX                             = 9, // QList<qreal>
    SBK_QtCharts_QList_QPointF_IDX                           = 10, // QList<QPointF>
    SBK_QtCharts_std_pair_qreal_qreal_IDX                    = 11, // std::pair<qreal,qreal>
    SBK_QtCharts_QHash_QXYSeries_PointConfiguration_QVariant_IDX = 12, // QHash<QXYSeries::PointConfiguration,QVariant>
    SBK_QtCharts_QHash_int_QHash_QXYSeries_PointConfiguration_QVariant_IDX = 13, // QHash<int,QHash<QXYSeries::PointConfiguration,QVariant>>
    SBK_QtCharts_QList_QPieSlicePTR_IDX                      = 14, // QList<QPieSlice*>
    SBK_QtCharts_QList_QCandlestickSetPTR_IDX                = 15, // QList<QCandlestickSet*>
    SBK_QtCharts_QList_QBoxSetPTR_IDX                        = 16, // QList<QBoxSet*>
    SBK_QtCharts_QList_QBarSetPTR_IDX                        = 17, // QList<QBarSet*>
    SBK_QtCharts_QList_QVariant_IDX                          = 18, // QList<QVariant>
    SBK_QtCharts_QList_QString_IDX                           = 19, // QList<QString>
    SBK_QtCharts_QMap_QString_QVariant_IDX                   = 20, // QMap<QString,QVariant>
    SBK_QtCharts_CONVERTERS_IDX_COUNT                        = 21,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QAbstractAxis::AxisType >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QAbstractAxis_AxisType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractAxis >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QAbstractAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractBarSeries::LabelsPosition >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QAbstractBarSeries_LabelsPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractBarSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QAbstractBarSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSeries::SeriesType >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QAbstractSeries_SeriesType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAbstractSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QAbstractSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAreaLegendMarker >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QAreaLegendMarker_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAreaSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QAreaSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBarCategoryAxis >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBarCategoryAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBarLegendMarker >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBarLegendMarker_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBarModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBarModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBarSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBarSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBarSet >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBarSet_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBoxPlotLegendMarker >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBoxPlotLegendMarker_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBoxPlotModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBoxPlotModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBoxPlotSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBoxPlotSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBoxSet::ValuePositions >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBoxSet_ValuePositions_IDX]); }
template<> inline PyTypeObject *SbkType< ::QBoxSet >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QBoxSet_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCandlestickLegendMarker >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QCandlestickLegendMarker_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCandlestickModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QCandlestickModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCandlestickSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QCandlestickSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCandlestickSet >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QCandlestickSet_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCategoryAxis::AxisLabelsPosition >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QCategoryAxis_AxisLabelsPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCategoryAxis >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QCategoryAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QChart::ChartType >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QChart_ChartType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QChart::ChartTheme >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QChart_ChartTheme_IDX]); }
template<> inline PyTypeObject *SbkType< ::QChart::AnimationOption >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QChart_AnimationOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QChart::AnimationOption> >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QFlags_QChart_AnimationOption_IDX]); }
template<> inline PyTypeObject *SbkType< ::QChart >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QChart_IDX]); }
template<> inline PyTypeObject *SbkType< ::QChartView::RubberBand >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QChartView_RubberBand_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QChartView::RubberBand> >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QFlags_QChartView_RubberBand_IDX]); }
template<> inline PyTypeObject *SbkType< ::QChartView >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QChartView_IDX]); }
template<> inline PyTypeObject *SbkType< ::QColorAxis >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QColorAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QDateTimeAxis >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QDateTimeAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHBarModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QHBarModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHBoxPlotModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QHBoxPlotModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHCandlestickModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QHCandlestickModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHPieModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QHPieModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHXYModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QHXYModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHorizontalBarSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QHorizontalBarSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHorizontalPercentBarSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QHorizontalPercentBarSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHorizontalStackedBarSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QHorizontalStackedBarSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLegend::MarkerShape >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QLegend_MarkerShape_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLegend >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QLegend_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLegendMarker::LegendMarkerType >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QLegendMarker_LegendMarkerType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLegendMarker >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QLegendMarker_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLineSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QLineSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLogValueAxis >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QLogValueAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPercentBarSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QPercentBarSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPieLegendMarker >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QPieLegendMarker_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPieModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QPieModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPieSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QPieSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPieSlice::LabelPosition >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QPieSlice_LabelPosition_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPieSlice >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QPieSlice_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPolarChart::PolarOrientation >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QPolarChart_PolarOrientation_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QPolarChart::PolarOrientation> >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QFlags_QPolarChart_PolarOrientation_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPolarChart >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QPolarChart_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScatterSeries::MarkerShape >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QScatterSeries_MarkerShape_IDX]); }
template<> inline PyTypeObject *SbkType< ::QScatterSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QScatterSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSplineSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QSplineSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QStackedBarSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QStackedBarSeries_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVBarModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QVBarModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVBoxPlotModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QVBoxPlotModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVCandlestickModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QVCandlestickModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVPieModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QVPieModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVXYModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QVXYModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QValueAxis::TickType >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QValueAxis_TickType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QValueAxis >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QValueAxis_IDX]); }
template<> inline PyTypeObject *SbkType< ::QXYLegendMarker >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QXYLegendMarker_IDX]); }
template<> inline PyTypeObject *SbkType< ::QXYModelMapper >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QXYModelMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QXYSeries::PointConfiguration >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QXYSeries_PointConfiguration_IDX]); }
template<> inline PyTypeObject *SbkType< ::QXYSeries >() { return Shiboken::Module::get(SbkPySide6_QtChartsTypeStructs[SBK_QXYSeries_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTCHARTS_PYTHON_H

