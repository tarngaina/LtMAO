// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QT3DEXTRAS_PYTHON_H
#define SBK_QT3DEXTRAS_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qt3drender_python.h>
#include <pyside6_qt3dcore_python.h>
#include <pyside6_qtgui_python.h>
#include <pyside6_qtcore_python.h>
#include <pyside6_qtopengl_python.h>

// Bound library includes
#include <Qt3DExtras/qabstractcameracontroller.h>

QT_BEGIN_NAMESPACE

namespace Qt3DExtras {
    class QAbstractSpriteSheet;
    class QConeGeometry;
    class QConeGeometryView;
    class QConeMesh;
    class QCuboidGeometry;
    class QCuboidGeometryView;
    class QCuboidMesh;
    class QCylinderGeometry;
    class QCylinderGeometryView;
    class QCylinderMesh;
    class QDiffuseMapMaterial;
    class QDiffuseSpecularMapMaterial;
    class QDiffuseSpecularMaterial;
    class QExtrudedTextGeometry;
    class QExtrudedTextMesh;
    class QFirstPersonCameraController;
    class QForwardRenderer;
    class QGoochMaterial;
    class QMetalRoughMaterial;
    class QMorphPhongMaterial;
    class QNormalDiffuseMapAlphaMaterial;
    class QNormalDiffuseMapMaterial;
    class QNormalDiffuseSpecularMapMaterial;
    class QOrbitCameraController;
    class QPerVertexColorMaterial;
    class QPhongAlphaMaterial;
    class QPhongMaterial;
    class QPlaneGeometry;
    class QPlaneGeometryView;
    class QPlaneMesh;
    class QSkyboxEntity;
    class QSphereGeometry;
    class QSphereGeometryView;
    class QSphereMesh;
    class QSpriteGrid;
    class QSpriteSheet;
    class QSpriteSheetItem;
    class QText2DEntity;
    class QTextureMaterial;
    class QTorusGeometry;
    class QTorusGeometryView;
    class QTorusMesh;
    class Qt3DWindow;
}
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QT3DEXTRASQT3DEXTRAS_IDX                             = 0,
    SBK_QT3DEXTRAS_QABSTRACTCAMERACONTROLLER_IDX             = 2,
    SBK_QT3DEXTRAS_QABSTRACTCAMERACONTROLLER_INPUTSTATE_IDX  = 4,
    SBK_QT3DEXTRAS_QABSTRACTSPRITESHEET_IDX                  = 6,
    SBK_QT3DEXTRAS_QCONEGEOMETRY_IDX                         = 8,
    SBK_QT3DEXTRAS_QCONEGEOMETRYVIEW_IDX                     = 10,
    SBK_QT3DEXTRAS_QCONEMESH_IDX                             = 12,
    SBK_QT3DEXTRAS_QCUBOIDGEOMETRY_IDX                       = 14,
    SBK_QT3DEXTRAS_QCUBOIDGEOMETRYVIEW_IDX                   = 16,
    SBK_QT3DEXTRAS_QCUBOIDMESH_IDX                           = 18,
    SBK_QT3DEXTRAS_QCYLINDERGEOMETRY_IDX                     = 20,
    SBK_QT3DEXTRAS_QCYLINDERGEOMETRYVIEW_IDX                 = 22,
    SBK_QT3DEXTRAS_QCYLINDERMESH_IDX                         = 24,
    SBK_QT3DEXTRAS_QDIFFUSEMAPMATERIAL_IDX                   = 26,
    SBK_QT3DEXTRAS_QDIFFUSESPECULARMAPMATERIAL_IDX           = 28,
    SBK_QT3DEXTRAS_QDIFFUSESPECULARMATERIAL_IDX              = 30,
    SBK_QT3DEXTRAS_QEXTRUDEDTEXTGEOMETRY_IDX                 = 32,
    SBK_QT3DEXTRAS_QEXTRUDEDTEXTMESH_IDX                     = 34,
    SBK_QT3DEXTRAS_QFIRSTPERSONCAMERACONTROLLER_IDX          = 36,
    SBK_QT3DEXTRAS_QFORWARDRENDERER_IDX                      = 38,
    SBK_QT3DEXTRAS_QGOOCHMATERIAL_IDX                        = 40,
    SBK_QT3DEXTRAS_QMETALROUGHMATERIAL_IDX                   = 42,
    SBK_QT3DEXTRAS_QMORPHPHONGMATERIAL_IDX                   = 44,
    SBK_QT3DEXTRAS_QNORMALDIFFUSEMAPALPHAMATERIAL_IDX        = 46,
    SBK_QT3DEXTRAS_QNORMALDIFFUSEMAPMATERIAL_IDX             = 48,
    SBK_QT3DEXTRAS_QNORMALDIFFUSESPECULARMAPMATERIAL_IDX     = 50,
    SBK_QT3DEXTRAS_QORBITCAMERACONTROLLER_IDX                = 52,
    SBK_QT3DEXTRAS_QPERVERTEXCOLORMATERIAL_IDX               = 54,
    SBK_QT3DEXTRAS_QPHONGALPHAMATERIAL_IDX                   = 56,
    SBK_QT3DEXTRAS_QPHONGMATERIAL_IDX                        = 58,
    SBK_QT3DEXTRAS_QPLANEGEOMETRY_IDX                        = 60,
    SBK_QT3DEXTRAS_QPLANEGEOMETRYVIEW_IDX                    = 62,
    SBK_QT3DEXTRAS_QPLANEMESH_IDX                            = 64,
    SBK_QT3DEXTRAS_QSKYBOXENTITY_IDX                         = 66,
    SBK_QT3DEXTRAS_QSPHEREGEOMETRY_IDX                       = 68,
    SBK_QT3DEXTRAS_QSPHEREGEOMETRYVIEW_IDX                   = 70,
    SBK_QT3DEXTRAS_QSPHEREMESH_IDX                           = 72,
    SBK_QT3DEXTRAS_QSPRITEGRID_IDX                           = 74,
    SBK_QT3DEXTRAS_QSPRITESHEET_IDX                          = 76,
    SBK_QT3DEXTRAS_QSPRITESHEETITEM_IDX                      = 78,
    SBK_QT3DEXTRAS_QTEXT2DENTITY_IDX                         = 80,
    SBK_QT3DEXTRAS_QTEXTUREMATERIAL_IDX                      = 82,
    SBK_QT3DEXTRAS_QTORUSGEOMETRY_IDX                        = 84,
    SBK_QT3DEXTRAS_QTORUSGEOMETRYVIEW_IDX                    = 86,
    SBK_QT3DEXTRAS_QTORUSMESH_IDX                            = 88,
    SBK_QT3DEXTRAS_QT3DWINDOW_IDX                            = 90,
    SBK_QT3DEXTRAS_IDX_COUNT                                 = 92,
};

// Type indices
enum : int {
    SBK_Qt3DExtrasQt3DExtras_IDX                             = 0,
    SBK_Qt3DExtras_QAbstractCameraController_IDX             = 1,
    SBK_Qt3DExtras_QAbstractCameraController_InputState_IDX  = 2,
    SBK_Qt3DExtras_QAbstractSpriteSheet_IDX                  = 3,
    SBK_Qt3DExtras_QConeGeometry_IDX                         = 4,
    SBK_Qt3DExtras_QConeGeometryView_IDX                     = 5,
    SBK_Qt3DExtras_QConeMesh_IDX                             = 6,
    SBK_Qt3DExtras_QCuboidGeometry_IDX                       = 7,
    SBK_Qt3DExtras_QCuboidGeometryView_IDX                   = 8,
    SBK_Qt3DExtras_QCuboidMesh_IDX                           = 9,
    SBK_Qt3DExtras_QCylinderGeometry_IDX                     = 10,
    SBK_Qt3DExtras_QCylinderGeometryView_IDX                 = 11,
    SBK_Qt3DExtras_QCylinderMesh_IDX                         = 12,
    SBK_Qt3DExtras_QDiffuseMapMaterial_IDX                   = 13,
    SBK_Qt3DExtras_QDiffuseSpecularMapMaterial_IDX           = 14,
    SBK_Qt3DExtras_QDiffuseSpecularMaterial_IDX              = 15,
    SBK_Qt3DExtras_QExtrudedTextGeometry_IDX                 = 16,
    SBK_Qt3DExtras_QExtrudedTextMesh_IDX                     = 17,
    SBK_Qt3DExtras_QFirstPersonCameraController_IDX          = 18,
    SBK_Qt3DExtras_QForwardRenderer_IDX                      = 19,
    SBK_Qt3DExtras_QGoochMaterial_IDX                        = 20,
    SBK_Qt3DExtras_QMetalRoughMaterial_IDX                   = 21,
    SBK_Qt3DExtras_QMorphPhongMaterial_IDX                   = 22,
    SBK_Qt3DExtras_QNormalDiffuseMapAlphaMaterial_IDX        = 23,
    SBK_Qt3DExtras_QNormalDiffuseMapMaterial_IDX             = 24,
    SBK_Qt3DExtras_QNormalDiffuseSpecularMapMaterial_IDX     = 25,
    SBK_Qt3DExtras_QOrbitCameraController_IDX                = 26,
    SBK_Qt3DExtras_QPerVertexColorMaterial_IDX               = 27,
    SBK_Qt3DExtras_QPhongAlphaMaterial_IDX                   = 28,
    SBK_Qt3DExtras_QPhongMaterial_IDX                        = 29,
    SBK_Qt3DExtras_QPlaneGeometry_IDX                        = 30,
    SBK_Qt3DExtras_QPlaneGeometryView_IDX                    = 31,
    SBK_Qt3DExtras_QPlaneMesh_IDX                            = 32,
    SBK_Qt3DExtras_QSkyboxEntity_IDX                         = 33,
    SBK_Qt3DExtras_QSphereGeometry_IDX                       = 34,
    SBK_Qt3DExtras_QSphereGeometryView_IDX                   = 35,
    SBK_Qt3DExtras_QSphereMesh_IDX                           = 36,
    SBK_Qt3DExtras_QSpriteGrid_IDX                           = 37,
    SBK_Qt3DExtras_QSpriteSheet_IDX                          = 38,
    SBK_Qt3DExtras_QSpriteSheetItem_IDX                      = 39,
    SBK_Qt3DExtras_QText2DEntity_IDX                         = 40,
    SBK_Qt3DExtras_QTextureMaterial_IDX                      = 41,
    SBK_Qt3DExtras_QTorusGeometry_IDX                        = 42,
    SBK_Qt3DExtras_QTorusGeometryView_IDX                    = 43,
    SBK_Qt3DExtras_QTorusMesh_IDX                            = 44,
    SBK_Qt3DExtras_Qt3DWindow_IDX                            = 45,
    SBK_Qt3DExtras_IDX_COUNT                                 = 46,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_Qt3DExtrasTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_Qt3DExtrasTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_Qt3DExtrasModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_Qt3DExtrasTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QT3DEXTRAS_QLIST_INT_IDX                             = 0, // QList<int>
    SBK_QT3DEXTRAS_QLIST_QT3DCORE_QCOMPONENTPTR_IDX          = 2, // QList<Qt3DCore::QComponent*>
    SBK_QT3DEXTRAS_QLIST_QT3DEXTRAS_QSPRITESHEETITEMPTR_IDX  = 4, // QList<Qt3DExtras::QSpriteSheetItem*>
    SBK_QT3DEXTRAS_QLIST_QT3DCORE_QNODEPTR_IDX               = 6, // QList<Qt3DCore::QNode*>
    SBK_QT3DEXTRAS_QLIST_QT3DCORE_QATTRIBUTEPTR_IDX          = 8, // QList<Qt3DCore::QAttribute*>
    SBK_QT3DEXTRAS_QLIST_QT3DRENDER_QPARAMETERPTR_IDX        = 10, // QList<Qt3DRender::QParameter*>
    SBK_QT3DEXTRAS_QLIST_QT3DRENDER_QFILTERKEYPTR_IDX        = 12, // QList<Qt3DRender::QFilterKey*>
    SBK_QT3DEXTRAS_QLIST_QVARIANT_IDX                        = 14, // QList<QVariant>
    SBK_QT3DEXTRAS_QLIST_QSTRING_IDX                         = 16, // QList<QString>
    SBK_QT3DEXTRAS_QMAP_QSTRING_QVARIANT_IDX                 = 18, // QMap<QString,QVariant>
    SBK_QT3DEXTRAS_CONVERTERS_IDX_COUNT                      = 20,
};

// Converter indices
enum : int {
    SBK_Qt3DExtras_QList_int_IDX                             = 0, // QList<int>
    SBK_Qt3DExtras_QList_Qt3DCore_QComponentPTR_IDX          = 1, // QList<Qt3DCore::QComponent*>
    SBK_Qt3DExtras_QList_Qt3DExtras_QSpriteSheetItemPTR_IDX  = 2, // QList<Qt3DExtras::QSpriteSheetItem*>
    SBK_Qt3DExtras_QList_Qt3DCore_QNodePTR_IDX               = 3, // QList<Qt3DCore::QNode*>
    SBK_Qt3DExtras_QList_Qt3DCore_QAttributePTR_IDX          = 4, // QList<Qt3DCore::QAttribute*>
    SBK_Qt3DExtras_QList_Qt3DRender_QParameterPTR_IDX        = 5, // QList<Qt3DRender::QParameter*>
    SBK_Qt3DExtras_QList_Qt3DRender_QFilterKeyPTR_IDX        = 6, // QList<Qt3DRender::QFilterKey*>
    SBK_Qt3DExtras_QList_QVariant_IDX                        = 7, // QList<QVariant>
    SBK_Qt3DExtras_QList_QString_IDX                         = 8, // QList<QString>
    SBK_Qt3DExtras_QMap_QString_QVariant_IDX                 = 9, // QMap<QString,QVariant>
    SBK_Qt3DExtras_CONVERTERS_IDX_COUNT                      = 10,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QAbstractCameraController >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QAbstractCameraController_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QAbstractCameraController::InputState >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QAbstractCameraController_InputState_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QAbstractSpriteSheet >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QAbstractSpriteSheet_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QConeGeometry >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QConeGeometry_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QConeGeometryView >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QConeGeometryView_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QConeMesh >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QConeMesh_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QCuboidGeometry >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QCuboidGeometry_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QCuboidGeometryView >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QCuboidGeometryView_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QCuboidMesh >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QCuboidMesh_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QCylinderGeometry >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QCylinderGeometry_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QCylinderGeometryView >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QCylinderGeometryView_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QCylinderMesh >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QCylinderMesh_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QDiffuseMapMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QDiffuseMapMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QDiffuseSpecularMapMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QDiffuseSpecularMapMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QDiffuseSpecularMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QDiffuseSpecularMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QExtrudedTextGeometry >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QExtrudedTextGeometry_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QExtrudedTextMesh >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QExtrudedTextMesh_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QFirstPersonCameraController >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QFirstPersonCameraController_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QForwardRenderer >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QForwardRenderer_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QGoochMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QGoochMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QMetalRoughMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QMetalRoughMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QMorphPhongMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QMorphPhongMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QNormalDiffuseMapAlphaMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QNormalDiffuseMapAlphaMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QNormalDiffuseMapMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QNormalDiffuseMapMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QNormalDiffuseSpecularMapMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QNormalDiffuseSpecularMapMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QOrbitCameraController >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QOrbitCameraController_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QPerVertexColorMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QPerVertexColorMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QPhongAlphaMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QPhongAlphaMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QPhongMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QPhongMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QPlaneGeometry >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QPlaneGeometry_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QPlaneGeometryView >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QPlaneGeometryView_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QPlaneMesh >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QPlaneMesh_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QSkyboxEntity >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QSkyboxEntity_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QSphereGeometry >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QSphereGeometry_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QSphereGeometryView >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QSphereGeometryView_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QSphereMesh >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QSphereMesh_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QSpriteGrid >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QSpriteGrid_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QSpriteSheet >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QSpriteSheet_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QSpriteSheetItem >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QSpriteSheetItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QText2DEntity >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QText2DEntity_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QTextureMaterial >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QTextureMaterial_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QTorusGeometry >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QTorusGeometry_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QTorusGeometryView >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QTorusGeometryView_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::QTorusMesh >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_QTorusMesh_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DExtras::Qt3DWindow >() { return Shiboken::Module::get(SbkPySide6_Qt3DExtrasTypeStructs[SBK_Qt3DExtras_Qt3DWindow_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QT3DEXTRAS_PYTHON_H

