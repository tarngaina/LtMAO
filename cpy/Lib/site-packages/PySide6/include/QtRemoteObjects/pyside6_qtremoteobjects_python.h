// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTREMOTEOBJECTS_PYTHON_H
#define SBK_QTREMOTEOBJECTS_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtcore_python.h>
#include <pyside6_qtnetwork_python.h>

// Bound library includes
#include <QtRemoteObjects/qremoteobjectnode.h>
#include <QtRemoteObjects/qremoteobjectpendingcall.h>
#include <QtRemoteObjects/qremoteobjectreplica.h>
#include <QtRemoteObjects/qtremoteobjectglobal.h>

QT_BEGIN_NAMESPACE
class QAbstractItemModelReplica;
class QConnectionAbstractServer;
class QRemoteObjectAbstractPersistedStore;
class QRemoteObjectDynamicReplica;
class QRemoteObjectHost;
class QRemoteObjectPendingCallWatcher;
class QRemoteObjectRegistry;
class QRemoteObjectRegistryHost;
class QRemoteObjectSettingsStore;
struct QRemoteObjectSourceLocationInfo;
class QtROClientFactory;
class QtROClientIoDevice;
class QtROIoDeviceBase;
class QtROServerFactory;
class QtROServerIoDevice;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QABSTRACTITEMMODELREPLICA_IDX                        = 0,
    SBK_QCONNECTIONABSTRACTSERVER_IDX                        = 2,
    SBK_QREMOTEOBJECTABSTRACTPERSISTEDSTORE_IDX              = 4,
    SBK_QREMOTEOBJECTDYNAMICREPLICA_IDX                      = 6,
    SBK_QREMOTEOBJECTHOST_IDX                                = 8,
    SBK_QREMOTEOBJECTHOSTBASE_ALLOWEDSCHEMAS_IDX             = 12,
    SBK_QREMOTEOBJECTHOSTBASE_IDX                            = 10,
    SBK_QREMOTEOBJECTNODE_ERRORCODE_IDX                      = 16,
    SBK_QREMOTEOBJECTNODE_IDX                                = 14,
    SBK_QREMOTEOBJECTPENDINGCALL_ERROR_IDX                   = 20,
    SBK_QREMOTEOBJECTPENDINGCALL_IDX                         = 18,
    SBK_QREMOTEOBJECTPENDINGCALLWATCHER_IDX                  = 22,
    SBK_QREMOTEOBJECTREGISTRY_IDX                            = 24,
    SBK_QREMOTEOBJECTREGISTRYHOST_IDX                        = 26,
    SBK_QREMOTEOBJECTREPLICA_STATE_IDX                       = 30,
    SBK_QREMOTEOBJECTREPLICA_IDX                             = 28,
    SBK_QREMOTEOBJECTSETTINGSSTORE_IDX                       = 32,
    SBK_QREMOTEOBJECTSOURCELOCATIONINFO_IDX                  = 34,
    SBK_QTROCLIENTFACTORY_IDX                                = 36,
    SBK_QTROCLIENTIODEVICE_IDX                               = 38,
    SBK_QTROIODEVICEBASE_IDX                                 = 40,
    SBK_QTROSERVERFACTORY_IDX                                = 42,
    SBK_QTROSERVERIODEVICE_IDX                               = 44,
    SBK_QTREMOTEOBJECTS_QREMOTEOBJECTPACKETTYPEENUM_IDX      = 50,
    SBK_QTREMOTEOBJECTS_INITIALACTION_IDX                    = 48,
    SBK_QTREMOTEOBJECTSQTREMOTEOBJECTS_IDX                   = 46,
    SBK_QTREMOTEOBJECTS_IDX_COUNT                            = 52,
};

// Type indices
enum : int {
    SBK_QAbstractItemModelReplica_IDX                        = 0,
    SBK_QConnectionAbstractServer_IDX                        = 1,
    SBK_QRemoteObjectAbstractPersistedStore_IDX              = 2,
    SBK_QRemoteObjectDynamicReplica_IDX                      = 3,
    SBK_QRemoteObjectHost_IDX                                = 4,
    SBK_QRemoteObjectHostBase_AllowedSchemas_IDX             = 6,
    SBK_QRemoteObjectHostBase_IDX                            = 5,
    SBK_QRemoteObjectNode_ErrorCode_IDX                      = 8,
    SBK_QRemoteObjectNode_IDX                                = 7,
    SBK_QRemoteObjectPendingCall_Error_IDX                   = 10,
    SBK_QRemoteObjectPendingCall_IDX                         = 9,
    SBK_QRemoteObjectPendingCallWatcher_IDX                  = 11,
    SBK_QRemoteObjectRegistry_IDX                            = 12,
    SBK_QRemoteObjectRegistryHost_IDX                        = 13,
    SBK_QRemoteObjectReplica_State_IDX                       = 15,
    SBK_QRemoteObjectReplica_IDX                             = 14,
    SBK_QRemoteObjectSettingsStore_IDX                       = 16,
    SBK_QRemoteObjectSourceLocationInfo_IDX                  = 17,
    SBK_QtROClientFactory_IDX                                = 18,
    SBK_QtROClientIoDevice_IDX                               = 19,
    SBK_QtROIoDeviceBase_IDX                                 = 20,
    SBK_QtROServerFactory_IDX                                = 21,
    SBK_QtROServerIoDevice_IDX                               = 22,
    SBK_QtRemoteObjects_QRemoteObjectPacketTypeEnum_IDX      = 25,
    SBK_QtRemoteObjects_InitialAction_IDX                    = 24,
    SBK_QtRemoteObjectsQtRemoteObjects_IDX                   = 23,
    SBK_QtRemoteObjects_IDX_COUNT                            = 26,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtRemoteObjectsTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtRemoteObjectsTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtRemoteObjectsModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtRemoteObjectsTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTREMOTEOBJECTS_QLIST_INT_IDX                        = 0, // QList<int>
    SBK_QTREMOTEOBJECTS_QLIST_QOBJECTPTR_IDX                 = 2, // QList<QObject*>
    SBK_QTREMOTEOBJECTS_QLIST_QBYTEARRAY_IDX                 = 4, // QList<QByteArray>
    SBK_QTREMOTEOBJECTS_QSET_QSTRING_IDX                     = 6, // QSet<QString>
    SBK_QTREMOTEOBJECTS_QLIST_QVARIANT_IDX                   = 8, // QList<QVariant>
    SBK_QTREMOTEOBJECTS_STD_PAIR_QSTRING_QREMOTEOBJECTSOURCELOCATIONINFO_IDX = 10, // std::pair<QString,QRemoteObjectSourceLocationInfo>
    SBK_QTREMOTEOBJECTS_QHASH_QSTRING_QREMOTEOBJECTSOURCELOCATIONINFO_IDX = 12, // QHash<QString,QRemoteObjectSourceLocationInfo>
    SBK_QTREMOTEOBJECTS_QLIST_QMODELINDEX_IDX                = 14, // QList<QModelIndex>
    SBK_QTREMOTEOBJECTS_QMAP_INT_QVARIANT_IDX                = 16, // QMap<int,QVariant>
    SBK_QTREMOTEOBJECTS_QHASH_INT_QBYTEARRAY_IDX             = 18, // QHash<int,QByteArray>
    SBK_QTREMOTEOBJECTS_QLIST_QSTRING_IDX                    = 20, // QList<QString>
    SBK_QTREMOTEOBJECTS_QMAP_QSTRING_QVARIANT_IDX            = 22, // QMap<QString,QVariant>
    SBK_QTREMOTEOBJECTS_CONVERTERS_IDX_COUNT                 = 24,
};

// Converter indices
enum : int {
    SBK_QtRemoteObjects_QList_int_IDX                        = 0, // QList<int>
    SBK_QtRemoteObjects_QList_QObjectPTR_IDX                 = 1, // QList<QObject*>
    SBK_QtRemoteObjects_QList_QByteArray_IDX                 = 2, // QList<QByteArray>
    SBK_QtRemoteObjects_QSet_QString_IDX                     = 3, // QSet<QString>
    SBK_QtRemoteObjects_QList_QVariant_IDX                   = 4, // QList<QVariant>
    SBK_QtRemoteObjects_std_pair_QString_QRemoteObjectSourceLocationInfo_IDX = 5, // std::pair<QString,QRemoteObjectSourceLocationInfo>
    SBK_QtRemoteObjects_QHash_QString_QRemoteObjectSourceLocationInfo_IDX = 6, // QHash<QString,QRemoteObjectSourceLocationInfo>
    SBK_QtRemoteObjects_QList_QModelIndex_IDX                = 7, // QList<QModelIndex>
    SBK_QtRemoteObjects_QMap_int_QVariant_IDX                = 8, // QMap<int,QVariant>
    SBK_QtRemoteObjects_QHash_int_QByteArray_IDX             = 9, // QHash<int,QByteArray>
    SBK_QtRemoteObjects_QList_QString_IDX                    = 10, // QList<QString>
    SBK_QtRemoteObjects_QMap_QString_QVariant_IDX            = 11, // QMap<QString,QVariant>
    SBK_QtRemoteObjects_CONVERTERS_IDX_COUNT                 = 12,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QAbstractItemModelReplica >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QAbstractItemModelReplica_IDX]); }
template<> inline PyTypeObject *SbkType< ::QConnectionAbstractServer >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QConnectionAbstractServer_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectAbstractPersistedStore >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectAbstractPersistedStore_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectDynamicReplica >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectDynamicReplica_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectHost >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectHost_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectHostBase::AllowedSchemas >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectHostBase_AllowedSchemas_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectHostBase >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectHostBase_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectNode::ErrorCode >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectNode_ErrorCode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectNode >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectNode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectPendingCall::Error >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectPendingCall_Error_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectPendingCall >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectPendingCall_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectPendingCallWatcher >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectPendingCallWatcher_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectRegistry >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectRegistry_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectRegistryHost >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectRegistryHost_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectReplica::State >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectReplica_State_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectReplica >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectReplica_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectSettingsStore >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectSettingsStore_IDX]); }
template<> inline PyTypeObject *SbkType< ::QRemoteObjectSourceLocationInfo >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QRemoteObjectSourceLocationInfo_IDX]); }
template<> inline PyTypeObject *SbkType< ::QtROClientFactory >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QtROClientFactory_IDX]); }
template<> inline PyTypeObject *SbkType< ::QtROClientIoDevice >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QtROClientIoDevice_IDX]); }
template<> inline PyTypeObject *SbkType< ::QtROIoDeviceBase >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QtROIoDeviceBase_IDX]); }
template<> inline PyTypeObject *SbkType< ::QtROServerFactory >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QtROServerFactory_IDX]); }
template<> inline PyTypeObject *SbkType< ::QtROServerIoDevice >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QtROServerIoDevice_IDX]); }
template<> inline PyTypeObject *SbkType< ::QtRemoteObjects::QRemoteObjectPacketTypeEnum >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QtRemoteObjects_QRemoteObjectPacketTypeEnum_IDX]); }
template<> inline PyTypeObject *SbkType< ::QtRemoteObjects::InitialAction >() { return Shiboken::Module::get(SbkPySide6_QtRemoteObjectsTypeStructs[SBK_QtRemoteObjects_InitialAction_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTREMOTEOBJECTS_PYTHON_H

