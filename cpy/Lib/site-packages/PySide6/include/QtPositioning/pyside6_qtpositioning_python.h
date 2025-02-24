// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTPOSITIONING_PYTHON_H
#define SBK_QTPOSITIONING_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QtPositioning/qgeoareamonitorsource.h>
#include <QtPositioning/qgeocoordinate.h>
#include <QtPositioning/qgeopositioninfo.h>
#include <QtPositioning/qgeopositioninfosource.h>
#include <QtPositioning/qgeosatelliteinfo.h>
#include <QtPositioning/qgeosatelliteinfosource.h>
#include <QtPositioning/qgeoshape.h>
#include <QtPositioning/qnmeapositioninfosource.h>
#include <QtPositioning/qnmeasatelliteinfosource.h>

QT_BEGIN_NAMESPACE
class QGeoAddress;
class QGeoAreaMonitorInfo;
class QGeoCircle;
class QGeoLocation;
class QGeoPath;
class QGeoPolygon;
class QGeoPositionInfoSourceFactory;
class QGeoRectangle;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QGEOADDRESS_IDX                                      = 4,
    SBK_QGEOAREAMONITORINFO_IDX                              = 6,
    SBK_QGEOAREAMONITORSOURCE_ERROR_IDX                      = 12,
    SBK_QGEOAREAMONITORSOURCE_AREAMONITORFEATURE_IDX         = 10,
    SBK_QFLAGS_QGEOAREAMONITORSOURCE_AREAMONITORFEATURE_IDX  = 0,
    SBK_QGEOAREAMONITORSOURCE_IDX                            = 8,
    SBK_QGEOCIRCLE_IDX                                       = 14,
    SBK_QGEOCOORDINATE_COORDINATETYPE_IDX                    = 20,
    SBK_QGEOCOORDINATE_COORDINATEFORMAT_IDX                  = 18,
    SBK_QGEOCOORDINATE_IDX                                   = 16,
    SBK_QGEOLOCATION_IDX                                     = 22,
    SBK_QGEOPATH_IDX                                         = 24,
    SBK_QGEOPOLYGON_IDX                                      = 26,
    SBK_QGEOPOSITIONINFO_ATTRIBUTE_IDX                       = 30,
    SBK_QGEOPOSITIONINFO_IDX                                 = 28,
    SBK_QGEOPOSITIONINFOSOURCE_ERROR_IDX                     = 34,
    SBK_QGEOPOSITIONINFOSOURCE_POSITIONINGMETHOD_IDX         = 36,
    SBK_QFLAGS_QGEOPOSITIONINFOSOURCE_POSITIONINGMETHOD_IDX  = 2,
    SBK_QGEOPOSITIONINFOSOURCE_IDX                           = 32,
    SBK_QGEOPOSITIONINFOSOURCEFACTORY_IDX                    = 38,
    SBK_QGEORECTANGLE_IDX                                    = 40,
    SBK_QGEOSATELLITEINFO_ATTRIBUTE_IDX                      = 44,
    SBK_QGEOSATELLITEINFO_SATELLITESYSTEM_IDX                = 46,
    SBK_QGEOSATELLITEINFO_IDX                                = 42,
    SBK_QGEOSATELLITEINFOSOURCE_ERROR_IDX                    = 50,
    SBK_QGEOSATELLITEINFOSOURCE_IDX                          = 48,
    SBK_QGEOSHAPE_SHAPETYPE_IDX                              = 54,
    SBK_QGEOSHAPE_IDX                                        = 52,
    SBK_QNMEAPOSITIONINFOSOURCE_UPDATEMODE_IDX               = 58,
    SBK_QNMEAPOSITIONINFOSOURCE_IDX                          = 56,
    SBK_QNMEASATELLITEINFOSOURCE_UPDATEMODE_IDX              = 64,
    SBK_QNMEASATELLITEINFOSOURCE_SATELLITEINFOPARSESTATUS_IDX = 62,
    SBK_QNMEASATELLITEINFOSOURCE_IDX                         = 60,
    SBK_QTPOSITIONING_IDX_COUNT                              = 66,
};

// Type indices
enum : int {
    SBK_QGeoAddress_IDX                                      = 2,
    SBK_QGeoAreaMonitorInfo_IDX                              = 3,
    SBK_QGeoAreaMonitorSource_Error_IDX                      = 6,
    SBK_QGeoAreaMonitorSource_AreaMonitorFeature_IDX         = 5,
    SBK_QFlags_QGeoAreaMonitorSource_AreaMonitorFeature_IDX  = 0,
    SBK_QGeoAreaMonitorSource_IDX                            = 4,
    SBK_QGeoCircle_IDX                                       = 7,
    SBK_QGeoCoordinate_CoordinateType_IDX                    = 10,
    SBK_QGeoCoordinate_CoordinateFormat_IDX                  = 9,
    SBK_QGeoCoordinate_IDX                                   = 8,
    SBK_QGeoLocation_IDX                                     = 11,
    SBK_QGeoPath_IDX                                         = 12,
    SBK_QGeoPolygon_IDX                                      = 13,
    SBK_QGeoPositionInfo_Attribute_IDX                       = 15,
    SBK_QGeoPositionInfo_IDX                                 = 14,
    SBK_QGeoPositionInfoSource_Error_IDX                     = 17,
    SBK_QGeoPositionInfoSource_PositioningMethod_IDX         = 18,
    SBK_QFlags_QGeoPositionInfoSource_PositioningMethod_IDX  = 1,
    SBK_QGeoPositionInfoSource_IDX                           = 16,
    SBK_QGeoPositionInfoSourceFactory_IDX                    = 19,
    SBK_QGeoRectangle_IDX                                    = 20,
    SBK_QGeoSatelliteInfo_Attribute_IDX                      = 22,
    SBK_QGeoSatelliteInfo_SatelliteSystem_IDX                = 23,
    SBK_QGeoSatelliteInfo_IDX                                = 21,
    SBK_QGeoSatelliteInfoSource_Error_IDX                    = 25,
    SBK_QGeoSatelliteInfoSource_IDX                          = 24,
    SBK_QGeoShape_ShapeType_IDX                              = 27,
    SBK_QGeoShape_IDX                                        = 26,
    SBK_QNmeaPositionInfoSource_UpdateMode_IDX               = 29,
    SBK_QNmeaPositionInfoSource_IDX                          = 28,
    SBK_QNmeaSatelliteInfoSource_UpdateMode_IDX              = 32,
    SBK_QNmeaSatelliteInfoSource_SatelliteInfoParseStatus_IDX = 31,
    SBK_QNmeaSatelliteInfoSource_IDX                         = 30,
    SBK_QtPositioning_IDX_COUNT                              = 33,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtPositioningTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtPositioningTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtPositioningModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtPositioningTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTPOSITIONING_QLIST_INT_IDX                          = 0, // QList<int>
    SBK_QTPOSITIONING_QLIST_QGEOCOORDINATE_IDX               = 2, // QList<QGeoCoordinate>
    SBK_QTPOSITIONING_QMAP_QSTRING_QVARIANT_IDX              = 4, // QMap<QString,QVariant>
    SBK_QTPOSITIONING_QLIST_QVARIANT_IDX                     = 6, // QList<QVariant>
    SBK_QTPOSITIONING_QLIST_QOBJECTPTR_IDX                   = 8, // QList<QObject*>
    SBK_QTPOSITIONING_QLIST_QBYTEARRAY_IDX                   = 10, // QList<QByteArray>
    SBK_QTPOSITIONING_QLIST_QGEOSATELLITEINFO_IDX            = 12, // QList<QGeoSatelliteInfo>
    SBK_QTPOSITIONING_QLIST_QGEOAREAMONITORINFO_IDX          = 14, // QList<QGeoAreaMonitorInfo>
    SBK_QTPOSITIONING_QLIST_QSTRING_IDX                      = 16, // QList<QString>
    SBK_QTPOSITIONING_CONVERTERS_IDX_COUNT                   = 18,
};

// Converter indices
enum : int {
    SBK_QtPositioning_QList_int_IDX                          = 0, // QList<int>
    SBK_QtPositioning_QList_QGeoCoordinate_IDX               = 1, // QList<QGeoCoordinate>
    SBK_QtPositioning_QMap_QString_QVariant_IDX              = 2, // QMap<QString,QVariant>
    SBK_QtPositioning_QList_QVariant_IDX                     = 3, // QList<QVariant>
    SBK_QtPositioning_QList_QObjectPTR_IDX                   = 4, // QList<QObject*>
    SBK_QtPositioning_QList_QByteArray_IDX                   = 5, // QList<QByteArray>
    SBK_QtPositioning_QList_QGeoSatelliteInfo_IDX            = 6, // QList<QGeoSatelliteInfo>
    SBK_QtPositioning_QList_QGeoAreaMonitorInfo_IDX          = 7, // QList<QGeoAreaMonitorInfo>
    SBK_QtPositioning_QList_QString_IDX                      = 8, // QList<QString>
    SBK_QtPositioning_CONVERTERS_IDX_COUNT                   = 9,
};
// Macros for type check

// Protected enum surrogates
enum PySide6_QtPositioning_QNmeaSatelliteInfoSource_SatelliteInfoParseStatus_Surrogate : int {};

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QGeoAddress >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoAddress_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoAreaMonitorInfo >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoAreaMonitorInfo_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoAreaMonitorSource::Error >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoAreaMonitorSource_Error_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoAreaMonitorSource::AreaMonitorFeature >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoAreaMonitorSource_AreaMonitorFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGeoAreaMonitorSource::AreaMonitorFeature> >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QFlags_QGeoAreaMonitorSource_AreaMonitorFeature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoAreaMonitorSource >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoAreaMonitorSource_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoCircle >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoCircle_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoCoordinate::CoordinateType >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoCoordinate_CoordinateType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoCoordinate::CoordinateFormat >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoCoordinate_CoordinateFormat_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoCoordinate >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoCoordinate_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoLocation >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoLocation_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoPath >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoPath_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoPolygon >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoPolygon_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoPositionInfo::Attribute >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoPositionInfo_Attribute_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoPositionInfo >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoPositionInfo_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoPositionInfoSource::Error >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoPositionInfoSource_Error_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoPositionInfoSource::PositioningMethod >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoPositionInfoSource_PositioningMethod_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QGeoPositionInfoSource::PositioningMethod> >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QFlags_QGeoPositionInfoSource_PositioningMethod_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoPositionInfoSource >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoPositionInfoSource_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoPositionInfoSourceFactory >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoPositionInfoSourceFactory_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoRectangle >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoRectangle_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoSatelliteInfo::Attribute >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoSatelliteInfo_Attribute_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoSatelliteInfo::SatelliteSystem >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoSatelliteInfo_SatelliteSystem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoSatelliteInfo >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoSatelliteInfo_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoSatelliteInfoSource::Error >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoSatelliteInfoSource_Error_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoSatelliteInfoSource >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoSatelliteInfoSource_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoShape::ShapeType >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoShape_ShapeType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGeoShape >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QGeoShape_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNmeaPositionInfoSource::UpdateMode >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QNmeaPositionInfoSource_UpdateMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNmeaPositionInfoSource >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QNmeaPositionInfoSource_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNmeaSatelliteInfoSource::UpdateMode >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QNmeaSatelliteInfoSource_UpdateMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::PySide6_QtPositioning_QNmeaSatelliteInfoSource_SatelliteInfoParseStatus_Surrogate >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QNmeaSatelliteInfoSource_SatelliteInfoParseStatus_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNmeaSatelliteInfoSource >() { return Shiboken::Module::get(SbkPySide6_QtPositioningTypeStructs[SBK_QNmeaSatelliteInfoSource_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTPOSITIONING_PYTHON_H

