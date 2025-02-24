// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTNFC_PYTHON_H
#define SBK_QTNFC_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QtNfc/qndeffilter.h>
#include <QtNfc/qndefnfcsmartposterrecord.h>
#include <QtNfc/qndefnfctextrecord.h>
#include <QtNfc/qndefrecord.h>
#include <QtNfc/qnearfieldmanager.h>
#include <QtNfc/qnearfieldtarget.h>

QT_BEGIN_NAMESPACE
class QNdefMessage;
class QNdefNfcIconRecord;
class QNdefNfcUriRecord;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QNDEFFILTER_IDX                                      = 2,
    SBK_QNDEFFILTER_RECORD_IDX                               = 4,
    SBK_QNDEFMESSAGE_IDX                                     = 6,
    SBK_QNDEFNFCICONRECORD_IDX                               = 8,
    SBK_QNDEFNFCSMARTPOSTERRECORD_ACTION_IDX                 = 12,
    SBK_QNDEFNFCSMARTPOSTERRECORD_IDX                        = 10,
    SBK_QNDEFNFCTEXTRECORD_ENCODING_IDX                      = 16,
    SBK_QNDEFNFCTEXTRECORD_IDX                               = 14,
    SBK_QNDEFNFCURIRECORD_IDX                                = 18,
    SBK_QNDEFRECORD_TYPENAMEFORMAT_IDX                       = 22,
    SBK_QNDEFRECORD_IDX                                      = 20,
    SBK_QNEARFIELDMANAGER_ADAPTERSTATE_IDX                   = 26,
    SBK_QNEARFIELDMANAGER_IDX                                = 24,
    SBK_QNEARFIELDTARGET_TYPE_IDX                            = 36,
    SBK_QNEARFIELDTARGET_ACCESSMETHOD_IDX                    = 30,
    SBK_QFLAGS_QNEARFIELDTARGET_ACCESSMETHOD_IDX             = 0,
    SBK_QNEARFIELDTARGET_ERROR_IDX                           = 32,
    SBK_QNEARFIELDTARGET_IDX                                 = 28,
    SBK_QNEARFIELDTARGET_REQUESTID_IDX                       = 34,
    SBK_QTNFC_IDX_COUNT                                      = 38,
};

// Type indices
enum : int {
    SBK_QNdefFilter_IDX                                      = 1,
    SBK_QNdefFilter_Record_IDX                               = 2,
    SBK_QNdefMessage_IDX                                     = 3,
    SBK_QNdefNfcIconRecord_IDX                               = 4,
    SBK_QNdefNfcSmartPosterRecord_Action_IDX                 = 6,
    SBK_QNdefNfcSmartPosterRecord_IDX                        = 5,
    SBK_QNdefNfcTextRecord_Encoding_IDX                      = 8,
    SBK_QNdefNfcTextRecord_IDX                               = 7,
    SBK_QNdefNfcUriRecord_IDX                                = 9,
    SBK_QNdefRecord_TypeNameFormat_IDX                       = 11,
    SBK_QNdefRecord_IDX                                      = 10,
    SBK_QNearFieldManager_AdapterState_IDX                   = 13,
    SBK_QNearFieldManager_IDX                                = 12,
    SBK_QNearFieldTarget_Type_IDX                            = 18,
    SBK_QNearFieldTarget_AccessMethod_IDX                    = 15,
    SBK_QFlags_QNearFieldTarget_AccessMethod_IDX             = 0,
    SBK_QNearFieldTarget_Error_IDX                           = 16,
    SBK_QNearFieldTarget_IDX                                 = 14,
    SBK_QNearFieldTarget_RequestId_IDX                       = 17,
    SBK_QtNfc_IDX_COUNT                                      = 19,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtNfcTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtNfcTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtNfcModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtNfcTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTNFC_QLIST_INT_IDX                                  = 0, // QList<int>
    SBK_QTNFC_QLIST_QNDEFRECORD_IDX                          = 2, // QList<QNdefRecord>
    SBK_QTNFC_QLIST_QOBJECTPTR_IDX                           = 4, // QList<QObject*>
    SBK_QTNFC_QLIST_QBYTEARRAY_IDX                           = 6, // QList<QByteArray>
    SBK_QTNFC_QLIST_QNDEFMESSAGE_IDX                         = 8, // QList<QNdefMessage>
    SBK_QTNFC_QLIST_QNDEFNFCICONRECORD_IDX                   = 10, // QList<QNdefNfcIconRecord>
    SBK_QTNFC_QLIST_QNDEFNFCTEXTRECORD_IDX                   = 12, // QList<QNdefNfcTextRecord>
    SBK_QTNFC_QLIST_QVARIANT_IDX                             = 14, // QList<QVariant>
    SBK_QTNFC_QLIST_QSTRING_IDX                              = 16, // QList<QString>
    SBK_QTNFC_QMAP_QSTRING_QVARIANT_IDX                      = 18, // QMap<QString,QVariant>
    SBK_QTNFC_CONVERTERS_IDX_COUNT                           = 20,
};

// Converter indices
enum : int {
    SBK_QtNfc_QList_int_IDX                                  = 0, // QList<int>
    SBK_QtNfc_QList_QNdefRecord_IDX                          = 1, // QList<QNdefRecord>
    SBK_QtNfc_QList_QObjectPTR_IDX                           = 2, // QList<QObject*>
    SBK_QtNfc_QList_QByteArray_IDX                           = 3, // QList<QByteArray>
    SBK_QtNfc_QList_QNdefMessage_IDX                         = 4, // QList<QNdefMessage>
    SBK_QtNfc_QList_QNdefNfcIconRecord_IDX                   = 5, // QList<QNdefNfcIconRecord>
    SBK_QtNfc_QList_QNdefNfcTextRecord_IDX                   = 6, // QList<QNdefNfcTextRecord>
    SBK_QtNfc_QList_QVariant_IDX                             = 7, // QList<QVariant>
    SBK_QtNfc_QList_QString_IDX                              = 8, // QList<QString>
    SBK_QtNfc_QMap_QString_QVariant_IDX                      = 9, // QMap<QString,QVariant>
    SBK_QtNfc_CONVERTERS_IDX_COUNT                           = 10,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QNdefFilter >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefFilter_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefFilter::Record >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefFilter_Record_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefMessage >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefMessage_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefNfcIconRecord >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefNfcIconRecord_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefNfcSmartPosterRecord::Action >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefNfcSmartPosterRecord_Action_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefNfcSmartPosterRecord >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefNfcSmartPosterRecord_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefNfcTextRecord::Encoding >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefNfcTextRecord_Encoding_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefNfcTextRecord >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefNfcTextRecord_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefNfcUriRecord >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefNfcUriRecord_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefRecord::TypeNameFormat >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefRecord_TypeNameFormat_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNdefRecord >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNdefRecord_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNearFieldManager::AdapterState >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNearFieldManager_AdapterState_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNearFieldManager >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNearFieldManager_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNearFieldTarget::Type >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNearFieldTarget_Type_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNearFieldTarget::AccessMethod >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNearFieldTarget_AccessMethod_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QNearFieldTarget::AccessMethod> >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QFlags_QNearFieldTarget_AccessMethod_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNearFieldTarget::Error >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNearFieldTarget_Error_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNearFieldTarget >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNearFieldTarget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QNearFieldTarget::RequestId >() { return Shiboken::Module::get(SbkPySide6_QtNfcTypeStructs[SBK_QNearFieldTarget_RequestId_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTNFC_PYTHON_H

