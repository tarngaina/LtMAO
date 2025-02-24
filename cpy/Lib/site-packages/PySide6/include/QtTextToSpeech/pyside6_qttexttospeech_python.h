// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTTEXTTOSPEECH_PYTHON_H
#define SBK_QTTEXTTOSPEECH_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QtTextToSpeech/qtexttospeech.h>
#include <QtTextToSpeech/qvoice.h>

QT_BEGIN_NAMESPACE
class QTextToSpeechEngine;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QTEXTTOSPEECH_STATE_IDX                              = 10,
    SBK_QTEXTTOSPEECH_ERRORREASON_IDX                        = 8,
    SBK_QTEXTTOSPEECH_BOUNDARYHINT_IDX                       = 4,
    SBK_QTEXTTOSPEECH_CAPABILITY_IDX                         = 6,
    SBK_QFLAGS_QTEXTTOSPEECH_CAPABILITY_IDX                  = 0,
    SBK_QTEXTTOSPEECH_IDX                                    = 2,
    SBK_QTEXTTOSPEECHENGINE_IDX                              = 12,
    SBK_QVOICE_GENDER_IDX                                    = 18,
    SBK_QVOICE_AGE_IDX                                       = 16,
    SBK_QVOICE_IDX                                           = 14,
    SBK_QTTEXTTOSPEECH_IDX_COUNT                             = 20,
};

// Type indices
enum : int {
    SBK_QTextToSpeech_State_IDX                              = 5,
    SBK_QTextToSpeech_ErrorReason_IDX                        = 4,
    SBK_QTextToSpeech_BoundaryHint_IDX                       = 2,
    SBK_QTextToSpeech_Capability_IDX                         = 3,
    SBK_QFlags_QTextToSpeech_Capability_IDX                  = 0,
    SBK_QTextToSpeech_IDX                                    = 1,
    SBK_QTextToSpeechEngine_IDX                              = 6,
    SBK_QVoice_Gender_IDX                                    = 9,
    SBK_QVoice_Age_IDX                                       = 8,
    SBK_QVoice_IDX                                           = 7,
    SBK_QtTextToSpeech_IDX_COUNT                             = 10,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtTextToSpeechTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtTextToSpeechTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtTextToSpeechModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtTextToSpeechTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTTEXTTOSPEECH_QLIST_INT_IDX                         = 0, // QList<int>
    SBK_QTTEXTTOSPEECH_QLIST_QLOCALE_IDX                     = 2, // QList<QLocale>
    SBK_QTTEXTTOSPEECH_QLIST_QVOICE_IDX                      = 4, // QList<QVoice>
    SBK_QTTEXTTOSPEECH_QLIST_QOBJECTPTR_IDX                  = 6, // QList<QObject*>
    SBK_QTTEXTTOSPEECH_QLIST_QBYTEARRAY_IDX                  = 8, // QList<QByteArray>
    SBK_QTTEXTTOSPEECH_QMAP_QSTRING_QVARIANT_IDX             = 10, // QMap<QString,QVariant>
    SBK_QTTEXTTOSPEECH_QLIST_QVARIANT_IDX                    = 12, // QList<QVariant>
    SBK_QTTEXTTOSPEECH_QLIST_QSTRING_IDX                     = 14, // QList<QString>
    SBK_QTTEXTTOSPEECH_CONVERTERS_IDX_COUNT                  = 16,
};

// Converter indices
enum : int {
    SBK_QtTextToSpeech_QList_int_IDX                         = 0, // QList<int>
    SBK_QtTextToSpeech_QList_QLocale_IDX                     = 1, // QList<QLocale>
    SBK_QtTextToSpeech_QList_QVoice_IDX                      = 2, // QList<QVoice>
    SBK_QtTextToSpeech_QList_QObjectPTR_IDX                  = 3, // QList<QObject*>
    SBK_QtTextToSpeech_QList_QByteArray_IDX                  = 4, // QList<QByteArray>
    SBK_QtTextToSpeech_QMap_QString_QVariant_IDX             = 5, // QMap<QString,QVariant>
    SBK_QtTextToSpeech_QList_QVariant_IDX                    = 6, // QList<QVariant>
    SBK_QtTextToSpeech_QList_QString_IDX                     = 7, // QList<QString>
    SBK_QtTextToSpeech_CONVERTERS_IDX_COUNT                  = 8,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QTextToSpeech::State >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QTextToSpeech_State_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextToSpeech::ErrorReason >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QTextToSpeech_ErrorReason_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextToSpeech::BoundaryHint >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QTextToSpeech_BoundaryHint_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextToSpeech::Capability >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QTextToSpeech_Capability_IDX]); }
template<> inline PyTypeObject *SbkType< ::QFlags<QTextToSpeech::Capability> >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QFlags_QTextToSpeech_Capability_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextToSpeech >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QTextToSpeech_IDX]); }
template<> inline PyTypeObject *SbkType< ::QTextToSpeechEngine >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QTextToSpeechEngine_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVoice::Gender >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QVoice_Gender_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVoice::Age >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QVoice_Age_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVoice >() { return Shiboken::Module::get(SbkPySide6_QtTextToSpeechTypeStructs[SBK_QVoice_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTTEXTTOSPEECH_PYTHON_H

