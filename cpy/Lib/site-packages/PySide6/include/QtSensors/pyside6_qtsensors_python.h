// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTSENSORS_PYTHON_H
#define SBK_QTSENSORS_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QtSensors/qaccelerometer.h>
#include <QtSensors/qambientlightsensor.h>
#include <QtSensors/qorientationsensor.h>
#include <QtSensors/qsensor.h>
#include <QtSensors/qtapsensor.h>

QT_BEGIN_NAMESPACE
class QAccelerometerFilter;
class QAccelerometerReading;
class QAmbientLightFilter;
class QAmbientLightSensor;
class QAmbientTemperatureFilter;
class QAmbientTemperatureReading;
class QAmbientTemperatureSensor;
class QCompass;
class QCompassFilter;
class QCompassReading;
class QGyroscope;
class QGyroscopeFilter;
class QGyroscopeReading;
class QHumidityFilter;
class QHumidityReading;
class QHumiditySensor;
class QIRProximityFilter;
class QIRProximityReading;
class QIRProximitySensor;
class QLidFilter;
class QLidReading;
class QLidSensor;
class QLightFilter;
class QLightReading;
class QLightSensor;
class QMagnetometer;
class QMagnetometerFilter;
class QMagnetometerReading;
class QOrientationFilter;
class QOrientationSensor;
class QPressureFilter;
class QPressureReading;
class QPressureSensor;
class QProximityFilter;
class QProximityReading;
class QProximitySensor;
class QRotationFilter;
class QRotationReading;
class QRotationSensor;
class QSensorBackend;
class QSensorBackendFactory;
class QSensorChangesInterface;
class QSensorFilter;
class QSensorManager;
class QSensorPluginInterface;
class QSensorReading;
class QTapFilter;
class QTapSensor;
class QTiltFilter;
class QTiltReading;
class QTiltSensor;
struct qoutputrange;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QACCELEROMETER_ACCELERATIONMODE_IDX                  = 2,
    SBK_QACCELEROMETER_IDX                                   = 0,
    SBK_QACCELEROMETERFILTER_IDX                             = 4,
    SBK_QACCELEROMETERREADING_IDX                            = 6,
    SBK_QAMBIENTLIGHTFILTER_IDX                              = 8,
    SBK_QAMBIENTLIGHTREADING_LIGHTLEVEL_IDX                  = 12,
    SBK_QAMBIENTLIGHTREADING_IDX                             = 10,
    SBK_QAMBIENTLIGHTSENSOR_IDX                              = 14,
    SBK_QAMBIENTTEMPERATUREFILTER_IDX                        = 16,
    SBK_QAMBIENTTEMPERATUREREADING_IDX                       = 18,
    SBK_QAMBIENTTEMPERATURESENSOR_IDX                        = 20,
    SBK_QCOMPASS_IDX                                         = 22,
    SBK_QCOMPASSFILTER_IDX                                   = 24,
    SBK_QCOMPASSREADING_IDX                                  = 26,
    SBK_QGYROSCOPE_IDX                                       = 28,
    SBK_QGYROSCOPEFILTER_IDX                                 = 30,
    SBK_QGYROSCOPEREADING_IDX                                = 32,
    SBK_QHUMIDITYFILTER_IDX                                  = 34,
    SBK_QHUMIDITYREADING_IDX                                 = 36,
    SBK_QHUMIDITYSENSOR_IDX                                  = 38,
    SBK_QIRPROXIMITYFILTER_IDX                               = 40,
    SBK_QIRPROXIMITYREADING_IDX                              = 42,
    SBK_QIRPROXIMITYSENSOR_IDX                               = 44,
    SBK_QLIDFILTER_IDX                                       = 46,
    SBK_QLIDREADING_IDX                                      = 48,
    SBK_QLIDSENSOR_IDX                                       = 50,
    SBK_QLIGHTFILTER_IDX                                     = 52,
    SBK_QLIGHTREADING_IDX                                    = 54,
    SBK_QLIGHTSENSOR_IDX                                     = 56,
    SBK_QMAGNETOMETER_IDX                                    = 58,
    SBK_QMAGNETOMETERFILTER_IDX                              = 60,
    SBK_QMAGNETOMETERREADING_IDX                             = 62,
    SBK_QORIENTATIONFILTER_IDX                               = 64,
    SBK_QORIENTATIONREADING_ORIENTATION_IDX                  = 68,
    SBK_QORIENTATIONREADING_IDX                              = 66,
    SBK_QORIENTATIONSENSOR_IDX                               = 70,
    SBK_QPRESSUREFILTER_IDX                                  = 72,
    SBK_QPRESSUREREADING_IDX                                 = 74,
    SBK_QPRESSURESENSOR_IDX                                  = 76,
    SBK_QPROXIMITYFILTER_IDX                                 = 78,
    SBK_QPROXIMITYREADING_IDX                                = 80,
    SBK_QPROXIMITYSENSOR_IDX                                 = 82,
    SBK_QROTATIONFILTER_IDX                                  = 84,
    SBK_QROTATIONREADING_IDX                                 = 86,
    SBK_QROTATIONSENSOR_IDX                                  = 88,
    SBK_QSENSOR_FEATURE_IDX                                  = 94,
    SBK_QSENSOR_AXESORIENTATIONMODE_IDX                      = 92,
    SBK_QSENSOR_IDX                                          = 90,
    SBK_QSENSORBACKEND_IDX                                   = 96,
    SBK_QSENSORBACKENDFACTORY_IDX                            = 98,
    SBK_QSENSORCHANGESINTERFACE_IDX                          = 100,
    SBK_QSENSORFILTER_IDX                                    = 102,
    SBK_QSENSORMANAGER_IDX                                   = 104,
    SBK_QSENSORPLUGININTERFACE_IDX                           = 106,
    SBK_QSENSORREADING_IDX                                   = 108,
    SBK_QTAPFILTER_IDX                                       = 110,
    SBK_QTAPREADING_TAPDIRECTION_IDX                         = 114,
    SBK_QTAPREADING_IDX                                      = 112,
    SBK_QTAPSENSOR_IDX                                       = 116,
    SBK_QTILTFILTER_IDX                                      = 118,
    SBK_QTILTREADING_IDX                                     = 120,
    SBK_QTILTSENSOR_IDX                                      = 122,
    SBK_QOUTPUTRANGE_IDX                                     = 124,
    SBK_QTSENSORS_IDX_COUNT                                  = 126,
};

// Type indices
enum : int {
    SBK_QAccelerometer_AccelerationMode_IDX                  = 1,
    SBK_QAccelerometer_IDX                                   = 0,
    SBK_QAccelerometerFilter_IDX                             = 2,
    SBK_QAccelerometerReading_IDX                            = 3,
    SBK_QAmbientLightFilter_IDX                              = 4,
    SBK_QAmbientLightReading_LightLevel_IDX                  = 6,
    SBK_QAmbientLightReading_IDX                             = 5,
    SBK_QAmbientLightSensor_IDX                              = 7,
    SBK_QAmbientTemperatureFilter_IDX                        = 8,
    SBK_QAmbientTemperatureReading_IDX                       = 9,
    SBK_QAmbientTemperatureSensor_IDX                        = 10,
    SBK_QCompass_IDX                                         = 11,
    SBK_QCompassFilter_IDX                                   = 12,
    SBK_QCompassReading_IDX                                  = 13,
    SBK_QGyroscope_IDX                                       = 14,
    SBK_QGyroscopeFilter_IDX                                 = 15,
    SBK_QGyroscopeReading_IDX                                = 16,
    SBK_QHumidityFilter_IDX                                  = 17,
    SBK_QHumidityReading_IDX                                 = 18,
    SBK_QHumiditySensor_IDX                                  = 19,
    SBK_QIRProximityFilter_IDX                               = 20,
    SBK_QIRProximityReading_IDX                              = 21,
    SBK_QIRProximitySensor_IDX                               = 22,
    SBK_QLidFilter_IDX                                       = 23,
    SBK_QLidReading_IDX                                      = 24,
    SBK_QLidSensor_IDX                                       = 25,
    SBK_QLightFilter_IDX                                     = 26,
    SBK_QLightReading_IDX                                    = 27,
    SBK_QLightSensor_IDX                                     = 28,
    SBK_QMagnetometer_IDX                                    = 29,
    SBK_QMagnetometerFilter_IDX                              = 30,
    SBK_QMagnetometerReading_IDX                             = 31,
    SBK_QOrientationFilter_IDX                               = 32,
    SBK_QOrientationReading_Orientation_IDX                  = 34,
    SBK_QOrientationReading_IDX                              = 33,
    SBK_QOrientationSensor_IDX                               = 35,
    SBK_QPressureFilter_IDX                                  = 36,
    SBK_QPressureReading_IDX                                 = 37,
    SBK_QPressureSensor_IDX                                  = 38,
    SBK_QProximityFilter_IDX                                 = 39,
    SBK_QProximityReading_IDX                                = 40,
    SBK_QProximitySensor_IDX                                 = 41,
    SBK_QRotationFilter_IDX                                  = 42,
    SBK_QRotationReading_IDX                                 = 43,
    SBK_QRotationSensor_IDX                                  = 44,
    SBK_QSensor_Feature_IDX                                  = 47,
    SBK_QSensor_AxesOrientationMode_IDX                      = 46,
    SBK_QSensor_IDX                                          = 45,
    SBK_QSensorBackend_IDX                                   = 48,
    SBK_QSensorBackendFactory_IDX                            = 49,
    SBK_QSensorChangesInterface_IDX                          = 50,
    SBK_QSensorFilter_IDX                                    = 51,
    SBK_QSensorManager_IDX                                   = 52,
    SBK_QSensorPluginInterface_IDX                           = 53,
    SBK_QSensorReading_IDX                                   = 54,
    SBK_QTapFilter_IDX                                       = 55,
    SBK_QTapReading_TapDirection_IDX                         = 57,
    SBK_QTapReading_IDX                                      = 56,
    SBK_QTapSensor_IDX                                       = 58,
    SBK_QTiltFilter_IDX                                      = 59,
    SBK_QTiltReading_IDX                                     = 60,
    SBK_QTiltSensor_IDX                                      = 61,
    SBK_qoutputrange_IDX                                     = 62,
    SBK_QtSensors_IDX_COUNT                                  = 63,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtSensorsTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtSensorsTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtSensorsModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtSensorsTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTSENSORS_QLIST_INT_IDX                              = 0, // QList<int>
    SBK_QTSENSORS_QLIST_QOBJECTPTR_IDX                       = 2, // QList<QObject*>
    SBK_QTSENSORS_QLIST_QBYTEARRAY_IDX                       = 4, // QList<QByteArray>
    SBK_QTSENSORS_STD_PAIR_INT_INT_IDX                       = 6, // std::pair<int,int>
    SBK_QTSENSORS_QLIST_STD_PAIR_INT_INT_IDX                 = 8, // QList<std::pair<int,int>>
    SBK_QTSENSORS_QLIST_QSENSORFILTERPTR_IDX                 = 10, // QList<QSensorFilter*>
    SBK_QTSENSORS_QLIST_QOUTPUTRANGE_IDX                     = 12, // QList<qoutputrange>
    SBK_QTSENSORS_QLIST_QVARIANT_IDX                         = 14, // QList<QVariant>
    SBK_QTSENSORS_QLIST_QSTRING_IDX                          = 16, // QList<QString>
    SBK_QTSENSORS_QMAP_QSTRING_QVARIANT_IDX                  = 18, // QMap<QString,QVariant>
    SBK_QTSENSORS_CONVERTERS_IDX_COUNT                       = 20,
};

// Converter indices
enum : int {
    SBK_QtSensors_QList_int_IDX                              = 0, // QList<int>
    SBK_QtSensors_QList_QObjectPTR_IDX                       = 1, // QList<QObject*>
    SBK_QtSensors_QList_QByteArray_IDX                       = 2, // QList<QByteArray>
    SBK_QtSensors_std_pair_int_int_IDX                       = 3, // std::pair<int,int>
    SBK_QtSensors_QList_std_pair_int_int_IDX                 = 4, // QList<std::pair<int,int>>
    SBK_QtSensors_QList_QSensorFilterPTR_IDX                 = 5, // QList<QSensorFilter*>
    SBK_QtSensors_QList_qoutputrange_IDX                     = 6, // QList<qoutputrange>
    SBK_QtSensors_QList_QVariant_IDX                         = 7, // QList<QVariant>
    SBK_QtSensors_QList_QString_IDX                          = 8, // QList<QString>
    SBK_QtSensors_QMap_QString_QVariant_IDX                  = 9, // QMap<QString,QVariant>
    SBK_QtSensors_CONVERTERS_IDX_COUNT                       = 10,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QAccelerometer::AccelerationMode >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAccelerometer_AccelerationMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAccelerometer >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAccelerometer_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAccelerometerFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAccelerometerFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAccelerometerReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAccelerometerReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAmbientLightFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAmbientLightFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAmbientLightReading::LightLevel >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAmbientLightReading_LightLevel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAmbientLightReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAmbientLightReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAmbientLightSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAmbientLightSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAmbientTemperatureFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAmbientTemperatureFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAmbientTemperatureReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAmbientTemperatureReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAmbientTemperatureSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QAmbientTemperatureSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCompass >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QCompass_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCompassFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QCompassFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QCompassReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QCompassReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGyroscope >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QGyroscope_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGyroscopeFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QGyroscopeFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QGyroscopeReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QGyroscopeReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHumidityFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QHumidityFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHumidityReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QHumidityReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QHumiditySensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QHumiditySensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QIRProximityFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QIRProximityFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QIRProximityReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QIRProximityReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QIRProximitySensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QIRProximitySensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLidFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QLidFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLidReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QLidReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLidSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QLidSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLightFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QLightFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLightReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QLightReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QLightSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QLightSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMagnetometer >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QMagnetometer_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMagnetometerFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QMagnetometerFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QMagnetometerReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QMagnetometerReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QOrientationFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QOrientationFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QOrientationReading::Orientation >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QOrientationReading_Orientation_IDX]); }
template<> inline PyTypeObject *SbkType< ::QOrientationReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QOrientationReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QOrientationSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QOrientationSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPressureFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QPressureFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPressureReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QPressureReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QPressureSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QPressureSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QProximityFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QProximityFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QProximityReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QProximityReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QProximitySensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QProximitySensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRotationFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QRotationFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRotationReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QRotationReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRotationSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QRotationSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensor::Feature >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensor_Feature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensor::AxesOrientationMode >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensor_AxesOrientationMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensorBackend >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensorBackend_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensorBackendFactory >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensorBackendFactory_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensorChangesInterface >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensorChangesInterface_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensorFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensorFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensorManager >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensorManager_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensorPluginInterface >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensorPluginInterface_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSensorReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QSensorReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTapFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QTapFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTapReading::TapDirection >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QTapReading_TapDirection_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTapReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QTapReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTapSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QTapSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTiltFilter >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QTiltFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTiltReading >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QTiltReading_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTiltSensor >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_QTiltSensor_IDX]); }
template<> inline PyTypeObject *SbkType< ::qoutputrange >() { return Shiboken::Module::get(SbkPySide6_QtSensorsTypeStructs[SBK_qoutputrange_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTSENSORS_PYTHON_H

