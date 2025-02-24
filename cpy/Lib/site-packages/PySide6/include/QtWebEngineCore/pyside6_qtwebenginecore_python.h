// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTWEBENGINECORE_PYTHON_H
#define SBK_QTWEBENGINECORE_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtcore_python.h>
#include <pyside6_qtgui_python.h>
#include <pyside6_qtnetwork_python.h>
#include <pyside6_qtprintsupport_python.h>
#include <pyside6_qtwidgets_python.h>
#include <pyside6_qtwebchannel_python.h>

// Bound library includes
#include <QtWebEngineCore/qwebenginecertificateerror.h>
#include <QtWebEngineCore/qwebenginecontextmenurequest.h>
#include <QtWebEngineCore/qwebenginecookiestore.h>
#include <QtWebEngineCore/qwebenginedownloadrequest.h>
#include <QtWebEngineCore/qwebenginefilesystemaccessrequest.h>
#include <QtWebEngineCore/qwebengineglobalsettings.h>
#include <QtWebEngineCore/qwebenginehistory.h>
#include <QtWebEngineCore/qwebenginehttprequest.h>
#include <QtWebEngineCore/qwebengineloadinginfo.h>
#include <QtWebEngineCore/qwebenginenavigationrequest.h>
#include <QtWebEngineCore/qwebenginenewwindowrequest.h>
#include <QtWebEngineCore/qwebenginepage.h>
#include <QtWebEngineCore/qwebenginepermission.h>
#include <QtWebEngineCore/qwebengineprofile.h>
#include <QtWebEngineCore/qwebenginescript.h>
#include <QtWebEngineCore/qwebenginesettings.h>
#include <QtWebEngineCore/qwebengineurlrequestinfo.h>
#include <QtWebEngineCore/qwebengineurlrequestjob.h>
#include <QtWebEngineCore/qwebengineurlscheme.h>
#include <QtWebEngineCore/qwebenginewebauthuxrequest.h>

QT_BEGIN_NAMESPACE
class QWebEngineClientCertificateSelection;
class QWebEngineClientCertificateStore;
class QWebEngineClientHints;
class QWebEngineDesktopMediaRequest;
class QWebEngineFindTextResult;
class QWebEngineFrame;
class QWebEngineFullScreenRequest;
class QWebEngineHistory;
class QWebEngineHistoryItem;
class QWebEngineNotification;
class QWebEngineQuotaRequest;
class QWebEngineRegisterProtocolHandlerRequest;
class QWebEngineScriptCollection;
class QWebEngineUrlRequestInterceptor;
class QWebEngineUrlSchemeHandler;
struct QWebEngineWebAuthPinRequest;

namespace QWebEngineGlobalSettings {
    struct DnsMode;
}
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QWEBENGINECERTIFICATEERROR_TYPE_IDX                  = 12,
    SBK_QWEBENGINECERTIFICATEERROR_IDX                       = 10,
    SBK_QWEBENGINECLIENTCERTIFICATESELECTION_IDX             = 14,
    SBK_QWEBENGINECLIENTCERTIFICATESTORE_IDX                 = 16,
    SBK_QWEBENGINECLIENTHINTS_IDX                            = 18,
    SBK_QWEBENGINECONTEXTMENUREQUEST_MEDIATYPE_IDX           = 26,
    SBK_QWEBENGINECONTEXTMENUREQUEST_MEDIAFLAG_IDX           = 24,
    SBK_QFLAGS_QWEBENGINECONTEXTMENUREQUEST_MEDIAFLAG_IDX    = 2,
    SBK_QWEBENGINECONTEXTMENUREQUEST_EDITFLAG_IDX            = 22,
    SBK_QFLAGS_QWEBENGINECONTEXTMENUREQUEST_EDITFLAG_IDX     = 0,
    SBK_QWEBENGINECONTEXTMENUREQUEST_IDX                     = 20,
    SBK_QWEBENGINECOOKIESTORE_IDX                            = 28,
    SBK_QWEBENGINECOOKIESTORE_FILTERREQUEST_IDX              = 30,
    SBK_QWEBENGINEDESKTOPMEDIAREQUEST_IDX                    = 32,
    SBK_QWEBENGINEDOWNLOADREQUEST_DOWNLOADSTATE_IDX          = 38,
    SBK_QWEBENGINEDOWNLOADREQUEST_SAVEPAGEFORMAT_IDX         = 40,
    SBK_QWEBENGINEDOWNLOADREQUEST_DOWNLOADINTERRUPTREASON_IDX = 36,
    SBK_QWEBENGINEDOWNLOADREQUEST_IDX                        = 34,
    SBK_QWEBENGINEFILESYSTEMACCESSREQUEST_HANDLETYPE_IDX     = 46,
    SBK_QWEBENGINEFILESYSTEMACCESSREQUEST_ACCESSFLAG_IDX     = 44,
    SBK_QFLAGS_QWEBENGINEFILESYSTEMACCESSREQUEST_ACCESSFLAG_IDX = 4,
    SBK_QWEBENGINEFILESYSTEMACCESSREQUEST_IDX                = 42,
    SBK_QWEBENGINEFINDTEXTRESULT_IDX                         = 48,
    SBK_QWEBENGINEFRAME_IDX                                  = 50,
    SBK_QWEBENGINEFULLSCREENREQUEST_IDX                      = 52,
    SBK_QWEBENGINEGLOBALSETTINGS_SECUREDNSMODE_IDX           = 58,
    SBK_QTWEBENGINECOREQWEBENGINEGLOBALSETTINGS_IDX          = 54,
    SBK_QWEBENGINEGLOBALSETTINGS_DNSMODE_IDX                 = 56,
    SBK_QWEBENGINEHISTORY_IDX                                = 60,
    SBK_QWEBENGINEHISTORYITEM_IDX                            = 62,
    SBK_QWEBENGINEHISTORYMODEL_ROLES_IDX                     = 66,
    SBK_QWEBENGINEHISTORYMODEL_IDX                           = 64,
    SBK_QWEBENGINEHTTPREQUEST_METHOD_IDX                     = 70,
    SBK_QWEBENGINEHTTPREQUEST_IDX                            = 68,
    SBK_QWEBENGINELOADINGINFO_LOADSTATUS_IDX                 = 76,
    SBK_QWEBENGINELOADINGINFO_ERRORDOMAIN_IDX                = 74,
    SBK_QWEBENGINELOADINGINFO_IDX                            = 72,
    SBK_QWEBENGINENAVIGATIONREQUEST_NAVIGATIONTYPE_IDX       = 82,
    SBK_QWEBENGINENAVIGATIONREQUEST_NAVIGATIONREQUESTACTION_IDX = 80,
    SBK_QWEBENGINENAVIGATIONREQUEST_IDX                      = 78,
    SBK_QWEBENGINENEWWINDOWREQUEST_DESTINATIONTYPE_IDX       = 86,
    SBK_QWEBENGINENEWWINDOWREQUEST_IDX                       = 84,
    SBK_QWEBENGINENOTIFICATION_IDX                           = 88,
    SBK_QWEBENGINEPAGE_WEBACTION_IDX                         = 108,
    SBK_QWEBENGINEPAGE_FINDFLAG_IDX                          = 96,
    SBK_QFLAGS_QWEBENGINEPAGE_FINDFLAG_IDX                   = 6,
    SBK_QWEBENGINEPAGE_WEBWINDOWTYPE_IDX                     = 110,
    SBK_QWEBENGINEPAGE_PERMISSIONPOLICY_IDX                  = 104,
    SBK_QWEBENGINEPAGE_NAVIGATIONTYPE_IDX                    = 102,
    SBK_QWEBENGINEPAGE_FEATURE_IDX                           = 92,
    SBK_QWEBENGINEPAGE_FILESELECTIONMODE_IDX                 = 94,
    SBK_QWEBENGINEPAGE_JAVASCRIPTCONSOLEMESSAGELEVEL_IDX     = 98,
    SBK_QWEBENGINEPAGE_RENDERPROCESSTERMINATIONSTATUS_IDX    = 106,
    SBK_QWEBENGINEPAGE_LIFECYCLESTATE_IDX                    = 100,
    SBK_QWEBENGINEPAGE_IDX                                   = 90,
    SBK_QWEBENGINEPERMISSION_PERMISSIONTYPE_IDX              = 114,
    SBK_QWEBENGINEPERMISSION_STATE_IDX                       = 116,
    SBK_QWEBENGINEPERMISSION_IDX                             = 112,
    SBK_QWEBENGINEPROFILE_HTTPCACHETYPE_IDX                  = 120,
    SBK_QWEBENGINEPROFILE_PERSISTENTCOOKIESPOLICY_IDX        = 122,
    SBK_QWEBENGINEPROFILE_PERSISTENTPERMISSIONSPOLICY_IDX    = 124,
    SBK_QWEBENGINEPROFILE_IDX                                = 118,
    SBK_QWEBENGINEQUOTAREQUEST_IDX                           = 126,
    SBK_QWEBENGINEREGISTERPROTOCOLHANDLERREQUEST_IDX         = 128,
    SBK_QWEBENGINESCRIPT_INJECTIONPOINT_IDX                  = 132,
    SBK_QWEBENGINESCRIPT_SCRIPTWORLDID_IDX                   = 134,
    SBK_QWEBENGINESCRIPT_IDX                                 = 130,
    SBK_QWEBENGINESCRIPTCOLLECTION_IDX                       = 136,
    SBK_QWEBENGINESETTINGS_FONTFAMILY_IDX                    = 140,
    SBK_QWEBENGINESETTINGS_WEBATTRIBUTE_IDX                  = 148,
    SBK_QWEBENGINESETTINGS_FONTSIZE_IDX                      = 142,
    SBK_QWEBENGINESETTINGS_UNKNOWNURLSCHEMEPOLICY_IDX        = 146,
    SBK_QWEBENGINESETTINGS_IMAGEANIMATIONPOLICY_IDX          = 144,
    SBK_QWEBENGINESETTINGS_IDX                               = 138,
    SBK_QWEBENGINEURLREQUESTINFO_RESOURCETYPE_IDX            = 154,
    SBK_QWEBENGINEURLREQUESTINFO_NAVIGATIONTYPE_IDX          = 152,
    SBK_QWEBENGINEURLREQUESTINFO_IDX                         = 150,
    SBK_QWEBENGINEURLREQUESTINTERCEPTOR_IDX                  = 156,
    SBK_QWEBENGINEURLREQUESTJOB_ERROR_IDX                    = 160,
    SBK_QWEBENGINEURLREQUESTJOB_IDX                          = 158,
    SBK_QWEBENGINEURLSCHEME_SYNTAX_IDX                       = 168,
    SBK_QWEBENGINEURLSCHEME_SPECIALPORT_IDX                  = 166,
    SBK_QWEBENGINEURLSCHEME_FLAG_IDX                         = 164,
    SBK_QFLAGS_QWEBENGINEURLSCHEME_FLAG_IDX                  = 8,
    SBK_QWEBENGINEURLSCHEME_IDX                              = 162,
    SBK_QWEBENGINEURLSCHEMEHANDLER_IDX                       = 170,
    SBK_QWEBENGINEWEBAUTHPINREQUEST_IDX                      = 172,
    SBK_QWEBENGINEWEBAUTHUXREQUEST_WEBAUTHUXSTATE_IDX        = 182,
    SBK_QWEBENGINEWEBAUTHUXREQUEST_PINENTRYREASON_IDX        = 178,
    SBK_QWEBENGINEWEBAUTHUXREQUEST_PINENTRYERROR_IDX         = 176,
    SBK_QWEBENGINEWEBAUTHUXREQUEST_REQUESTFAILUREREASON_IDX  = 180,
    SBK_QWEBENGINEWEBAUTHUXREQUEST_IDX                       = 174,
    SBK_QTWEBENGINECORE_IDX_COUNT                            = 184,
};

// Type indices
enum : int {
    SBK_QWebEngineCertificateError_Type_IDX                  = 6,
    SBK_QWebEngineCertificateError_IDX                       = 5,
    SBK_QWebEngineClientCertificateSelection_IDX             = 7,
    SBK_QWebEngineClientCertificateStore_IDX                 = 8,
    SBK_QWebEngineClientHints_IDX                            = 9,
    SBK_QWebEngineContextMenuRequest_MediaType_IDX           = 13,
    SBK_QWebEngineContextMenuRequest_MediaFlag_IDX           = 12,
    SBK_QFlags_QWebEngineContextMenuRequest_MediaFlag_IDX    = 1,
    SBK_QWebEngineContextMenuRequest_EditFlag_IDX            = 11,
    SBK_QFlags_QWebEngineContextMenuRequest_EditFlag_IDX     = 0,
    SBK_QWebEngineContextMenuRequest_IDX                     = 10,
    SBK_QWebEngineCookieStore_IDX                            = 14,
    SBK_QWebEngineCookieStore_FilterRequest_IDX              = 15,
    SBK_QWebEngineDesktopMediaRequest_IDX                    = 16,
    SBK_QWebEngineDownloadRequest_DownloadState_IDX          = 19,
    SBK_QWebEngineDownloadRequest_SavePageFormat_IDX         = 20,
    SBK_QWebEngineDownloadRequest_DownloadInterruptReason_IDX = 18,
    SBK_QWebEngineDownloadRequest_IDX                        = 17,
    SBK_QWebEngineFileSystemAccessRequest_HandleType_IDX     = 23,
    SBK_QWebEngineFileSystemAccessRequest_AccessFlag_IDX     = 22,
    SBK_QFlags_QWebEngineFileSystemAccessRequest_AccessFlag_IDX = 2,
    SBK_QWebEngineFileSystemAccessRequest_IDX                = 21,
    SBK_QWebEngineFindTextResult_IDX                         = 24,
    SBK_QWebEngineFrame_IDX                                  = 25,
    SBK_QWebEngineFullScreenRequest_IDX                      = 26,
    SBK_QWebEngineGlobalSettings_SecureDnsMode_IDX           = 29,
    SBK_QtWebEngineCoreQWebEngineGlobalSettings_IDX          = 27,
    SBK_QWebEngineGlobalSettings_DnsMode_IDX                 = 28,
    SBK_QWebEngineHistory_IDX                                = 30,
    SBK_QWebEngineHistoryItem_IDX                            = 31,
    SBK_QWebEngineHistoryModel_Roles_IDX                     = 33,
    SBK_QWebEngineHistoryModel_IDX                           = 32,
    SBK_QWebEngineHttpRequest_Method_IDX                     = 35,
    SBK_QWebEngineHttpRequest_IDX                            = 34,
    SBK_QWebEngineLoadingInfo_LoadStatus_IDX                 = 38,
    SBK_QWebEngineLoadingInfo_ErrorDomain_IDX                = 37,
    SBK_QWebEngineLoadingInfo_IDX                            = 36,
    SBK_QWebEngineNavigationRequest_NavigationType_IDX       = 41,
    SBK_QWebEngineNavigationRequest_NavigationRequestAction_IDX = 40,
    SBK_QWebEngineNavigationRequest_IDX                      = 39,
    SBK_QWebEngineNewWindowRequest_DestinationType_IDX       = 43,
    SBK_QWebEngineNewWindowRequest_IDX                       = 42,
    SBK_QWebEngineNotification_IDX                           = 44,
    SBK_QWebEnginePage_WebAction_IDX                         = 54,
    SBK_QWebEnginePage_FindFlag_IDX                          = 48,
    SBK_QFlags_QWebEnginePage_FindFlag_IDX                   = 3,
    SBK_QWebEnginePage_WebWindowType_IDX                     = 55,
    SBK_QWebEnginePage_PermissionPolicy_IDX                  = 52,
    SBK_QWebEnginePage_NavigationType_IDX                    = 51,
    SBK_QWebEnginePage_Feature_IDX                           = 46,
    SBK_QWebEnginePage_FileSelectionMode_IDX                 = 47,
    SBK_QWebEnginePage_JavaScriptConsoleMessageLevel_IDX     = 49,
    SBK_QWebEnginePage_RenderProcessTerminationStatus_IDX    = 53,
    SBK_QWebEnginePage_LifecycleState_IDX                    = 50,
    SBK_QWebEnginePage_IDX                                   = 45,
    SBK_QWebEnginePermission_PermissionType_IDX              = 57,
    SBK_QWebEnginePermission_State_IDX                       = 58,
    SBK_QWebEnginePermission_IDX                             = 56,
    SBK_QWebEngineProfile_HttpCacheType_IDX                  = 60,
    SBK_QWebEngineProfile_PersistentCookiesPolicy_IDX        = 61,
    SBK_QWebEngineProfile_PersistentPermissionsPolicy_IDX    = 62,
    SBK_QWebEngineProfile_IDX                                = 59,
    SBK_QWebEngineQuotaRequest_IDX                           = 63,
    SBK_QWebEngineRegisterProtocolHandlerRequest_IDX         = 64,
    SBK_QWebEngineScript_InjectionPoint_IDX                  = 66,
    SBK_QWebEngineScript_ScriptWorldId_IDX                   = 67,
    SBK_QWebEngineScript_IDX                                 = 65,
    SBK_QWebEngineScriptCollection_IDX                       = 68,
    SBK_QWebEngineSettings_FontFamily_IDX                    = 70,
    SBK_QWebEngineSettings_WebAttribute_IDX                  = 74,
    SBK_QWebEngineSettings_FontSize_IDX                      = 71,
    SBK_QWebEngineSettings_UnknownUrlSchemePolicy_IDX        = 73,
    SBK_QWebEngineSettings_ImageAnimationPolicy_IDX          = 72,
    SBK_QWebEngineSettings_IDX                               = 69,
    SBK_QWebEngineUrlRequestInfo_ResourceType_IDX            = 77,
    SBK_QWebEngineUrlRequestInfo_NavigationType_IDX          = 76,
    SBK_QWebEngineUrlRequestInfo_IDX                         = 75,
    SBK_QWebEngineUrlRequestInterceptor_IDX                  = 78,
    SBK_QWebEngineUrlRequestJob_Error_IDX                    = 80,
    SBK_QWebEngineUrlRequestJob_IDX                          = 79,
    SBK_QWebEngineUrlScheme_Syntax_IDX                       = 84,
    SBK_QWebEngineUrlScheme_SpecialPort_IDX                  = 83,
    SBK_QWebEngineUrlScheme_Flag_IDX                         = 82,
    SBK_QFlags_QWebEngineUrlScheme_Flag_IDX                  = 4,
    SBK_QWebEngineUrlScheme_IDX                              = 81,
    SBK_QWebEngineUrlSchemeHandler_IDX                       = 85,
    SBK_QWebEngineWebAuthPinRequest_IDX                      = 86,
    SBK_QWebEngineWebAuthUxRequest_WebAuthUxState_IDX        = 91,
    SBK_QWebEngineWebAuthUxRequest_PinEntryReason_IDX        = 89,
    SBK_QWebEngineWebAuthUxRequest_PinEntryError_IDX         = 88,
    SBK_QWebEngineWebAuthUxRequest_RequestFailureReason_IDX  = 90,
    SBK_QWebEngineWebAuthUxRequest_IDX                       = 87,
    SBK_QtWebEngineCore_IDX_COUNT                            = 92,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtWebEngineCoreTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtWebEngineCoreTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtWebEngineCoreModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtWebEngineCoreTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTWEBENGINECORE_QLIST_INT_IDX                        = 0, // QList<int>
    SBK_QTWEBENGINECORE_QHASH_QBYTEARRAY_QBYTEARRAY_IDX      = 2, // QHash<QByteArray,QByteArray>
    SBK_QTWEBENGINECORE_QLIST_QWEBENGINESCRIPT_IDX           = 4, // QList<QWebEngineScript>
    SBK_QTWEBENGINECORE_QMULTIMAP_QBYTEARRAY_QBYTEARRAY_IDX  = 6, // QMultiMap<QByteArray,QByteArray>
    SBK_QTWEBENGINECORE_QLIST_QWEBENGINEFRAME_IDX            = 8, // QList<QWebEngineFrame>
    SBK_QTWEBENGINECORE_QLIST_QSSLCERTIFICATE_IDX            = 10, // QList<QSslCertificate>
    SBK_QTWEBENGINECORE_QLIST_QOBJECTPTR_IDX                 = 12, // QList<QObject*>
    SBK_QTWEBENGINECORE_QLIST_QBYTEARRAY_IDX                 = 14, // QList<QByteArray>
    SBK_QTWEBENGINECORE_QMAP_QBYTEARRAY_QBYTEARRAY_IDX       = 16, // QMap<QByteArray,QByteArray>
    SBK_QTWEBENGINECORE_QLIST_QURL_IDX                       = 18, // QList<QUrl>
    SBK_QTWEBENGINECORE_QLIST_QWEBENGINEPERMISSION_IDX       = 20, // QList<QWebEnginePermission>
    SBK_QTWEBENGINECORE_QLIST_QWEBENGINEHISTORYITEM_IDX      = 22, // QList<QWebEngineHistoryItem>
    SBK_QTWEBENGINECORE_QMAP_QSTRING_QVARIANT_IDX            = 24, // QMap<QString,QVariant>
    SBK_QTWEBENGINECORE_STD_PAIR_BOOL_QSTRING_IDX            = 26, // std::pair<bool,QString>
    SBK_QTWEBENGINECORE_QMAP_QSTRING_QSTRING_IDX             = 28, // QMap<QString,QString>
    SBK_QTWEBENGINECORE_QMAP_INT_QVARIANT_IDX                = 30, // QMap<int,QVariant>
    SBK_QTWEBENGINECORE_QLIST_QMODELINDEX_IDX                = 32, // QList<QModelIndex>
    SBK_QTWEBENGINECORE_QHASH_INT_QBYTEARRAY_IDX             = 34, // QHash<int,QByteArray>
    SBK_QTWEBENGINECORE_QLIST_QVARIANT_IDX                   = 36, // QList<QVariant>
    SBK_QTWEBENGINECORE_QLIST_QSTRING_IDX                    = 38, // QList<QString>
    SBK_QTWEBENGINECORE_CONVERTERS_IDX_COUNT                 = 40,
};

// Converter indices
enum : int {
    SBK_QtWebEngineCore_QList_int_IDX                        = 0, // QList<int>
    SBK_QtWebEngineCore_QHash_QByteArray_QByteArray_IDX      = 1, // QHash<QByteArray,QByteArray>
    SBK_QtWebEngineCore_QList_QWebEngineScript_IDX           = 2, // QList<QWebEngineScript>
    SBK_QtWebEngineCore_QMultiMap_QByteArray_QByteArray_IDX  = 3, // QMultiMap<QByteArray,QByteArray>
    SBK_QtWebEngineCore_QList_QWebEngineFrame_IDX            = 4, // QList<QWebEngineFrame>
    SBK_QtWebEngineCore_QList_QSslCertificate_IDX            = 5, // QList<QSslCertificate>
    SBK_QtWebEngineCore_QList_QObjectPTR_IDX                 = 6, // QList<QObject*>
    SBK_QtWebEngineCore_QList_QByteArray_IDX                 = 7, // QList<QByteArray>
    SBK_QtWebEngineCore_QMap_QByteArray_QByteArray_IDX       = 8, // QMap<QByteArray,QByteArray>
    SBK_QtWebEngineCore_QList_QUrl_IDX                       = 9, // QList<QUrl>
    SBK_QtWebEngineCore_QList_QWebEnginePermission_IDX       = 10, // QList<QWebEnginePermission>
    SBK_QtWebEngineCore_QList_QWebEngineHistoryItem_IDX      = 11, // QList<QWebEngineHistoryItem>
    SBK_QtWebEngineCore_QMap_QString_QVariant_IDX            = 12, // QMap<QString,QVariant>
    SBK_QtWebEngineCore_std_pair_bool_QString_IDX            = 13, // std::pair<bool,QString>
    SBK_QtWebEngineCore_QMap_QString_QString_IDX             = 14, // QMap<QString,QString>
    SBK_QtWebEngineCore_QMap_int_QVariant_IDX                = 15, // QMap<int,QVariant>
    SBK_QtWebEngineCore_QList_QModelIndex_IDX                = 16, // QList<QModelIndex>
    SBK_QtWebEngineCore_QHash_int_QByteArray_IDX             = 17, // QHash<int,QByteArray>
    SBK_QtWebEngineCore_QList_QVariant_IDX                   = 18, // QList<QVariant>
    SBK_QtWebEngineCore_QList_QString_IDX                    = 19, // QList<QString>
    SBK_QtWebEngineCore_CONVERTERS_IDX_COUNT                 = 20,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QWebEngineCertificateError::Type >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineCertificateError_Type_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineCertificateError >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineCertificateError_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineClientCertificateSelection >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineClientCertificateSelection_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineClientCertificateStore >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineClientCertificateStore_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineClientHints >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineClientHints_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineContextMenuRequest::MediaType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineContextMenuRequest_MediaType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineContextMenuRequest::MediaFlag >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineContextMenuRequest_MediaFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QWebEngineContextMenuRequest::MediaFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QFlags_QWebEngineContextMenuRequest_MediaFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineContextMenuRequest::EditFlag >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineContextMenuRequest_EditFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QWebEngineContextMenuRequest::EditFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QFlags_QWebEngineContextMenuRequest_EditFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineContextMenuRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineContextMenuRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineCookieStore >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineCookieStore_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineCookieStore::FilterRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineCookieStore_FilterRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineDesktopMediaRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineDesktopMediaRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineDownloadRequest::DownloadState >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineDownloadRequest_DownloadState_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineDownloadRequest::SavePageFormat >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineDownloadRequest_SavePageFormat_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineDownloadRequest::DownloadInterruptReason >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineDownloadRequest_DownloadInterruptReason_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineDownloadRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineDownloadRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineFileSystemAccessRequest::HandleType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineFileSystemAccessRequest_HandleType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineFileSystemAccessRequest::AccessFlag >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineFileSystemAccessRequest_AccessFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QWebEngineFileSystemAccessRequest::AccessFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QFlags_QWebEngineFileSystemAccessRequest_AccessFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineFileSystemAccessRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineFileSystemAccessRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineFindTextResult >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineFindTextResult_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineFrame >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineFrame_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineFullScreenRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineFullScreenRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineGlobalSettings::SecureDnsMode >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineGlobalSettings_SecureDnsMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineGlobalSettings::DnsMode >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineGlobalSettings_DnsMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineHistory >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineHistory_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineHistoryItem >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineHistoryItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineHistoryModel::Roles >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineHistoryModel_Roles_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineHistoryModel >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineHistoryModel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineHttpRequest::Method >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineHttpRequest_Method_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineHttpRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineHttpRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineLoadingInfo::LoadStatus >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineLoadingInfo_LoadStatus_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineLoadingInfo::ErrorDomain >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineLoadingInfo_ErrorDomain_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineLoadingInfo >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineLoadingInfo_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineNavigationRequest::NavigationType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineNavigationRequest_NavigationType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineNavigationRequest::NavigationRequestAction >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineNavigationRequest_NavigationRequestAction_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineNavigationRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineNavigationRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineNewWindowRequest::DestinationType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineNewWindowRequest_DestinationType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineNewWindowRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineNewWindowRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineNotification >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineNotification_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::WebAction >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_WebAction_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::FindFlag >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_FindFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QWebEnginePage::FindFlag> >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QFlags_QWebEnginePage_FindFlag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::WebWindowType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_WebWindowType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::PermissionPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_PermissionPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::NavigationType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_NavigationType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::Feature >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_Feature_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::FileSelectionMode >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_FileSelectionMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::JavaScriptConsoleMessageLevel >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_JavaScriptConsoleMessageLevel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::RenderProcessTerminationStatus >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_RenderProcessTerminationStatus_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage::LifecycleState >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_LifecycleState_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePage >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePage_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePermission::PermissionType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePermission_PermissionType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePermission::State >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePermission_State_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEnginePermission >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEnginePermission_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineProfile::HttpCacheType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineProfile_HttpCacheType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineProfile::PersistentCookiesPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineProfile_PersistentCookiesPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineProfile::PersistentPermissionsPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineProfile_PersistentPermissionsPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineProfile >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineProfile_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineQuotaRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineQuotaRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineRegisterProtocolHandlerRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineRegisterProtocolHandlerRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineScript::InjectionPoint >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineScript_InjectionPoint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineScript::ScriptWorldId >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineScript_ScriptWorldId_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineScript >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineScript_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineScriptCollection >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineScriptCollection_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineSettings::FontFamily >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineSettings_FontFamily_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineSettings::WebAttribute >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineSettings_WebAttribute_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineSettings::FontSize >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineSettings_FontSize_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineSettings::UnknownUrlSchemePolicy >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineSettings_UnknownUrlSchemePolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineSettings::ImageAnimationPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineSettings_ImageAnimationPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineSettings >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineSettings_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlRequestInfo::ResourceType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlRequestInfo_ResourceType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlRequestInfo::NavigationType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlRequestInfo_NavigationType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlRequestInfo >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlRequestInfo_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlRequestInterceptor >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlRequestInterceptor_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlRequestJob::Error >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlRequestJob_Error_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlRequestJob >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlRequestJob_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlScheme::Syntax >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlScheme_Syntax_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlScheme::SpecialPort >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlScheme_SpecialPort_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlScheme::Flag >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlScheme_Flag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QWebEngineUrlScheme::Flag> >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QFlags_QWebEngineUrlScheme_Flag_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlScheme >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlScheme_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineUrlSchemeHandler >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineUrlSchemeHandler_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineWebAuthPinRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineWebAuthPinRequest_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineWebAuthUxRequest::WebAuthUxState >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineWebAuthUxRequest_WebAuthUxState_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineWebAuthUxRequest::PinEntryReason >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineWebAuthUxRequest_PinEntryReason_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineWebAuthUxRequest::PinEntryError >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineWebAuthUxRequest_PinEntryError_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineWebAuthUxRequest::RequestFailureReason >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineWebAuthUxRequest_RequestFailureReason_IDX]); }
template<> inline PyTypeObject *SbkType< ::QWebEngineWebAuthUxRequest >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineCoreTypeStructs[SBK_QWebEngineWebAuthUxRequest_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTWEBENGINECORE_PYTHON_H

