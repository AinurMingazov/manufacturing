from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from cost.models import (AssemblyDetail, AssemblyLabor, AssemblyMaterial,
                         AssemblyStandardDetail, DetailLabor, DetailMaterial,
                         ManufacturingPlan, MPAssembly, MPDetail, MPLabor,
                         MPProduct, MPResources, MPResourcesLabor,
                         MPResourcesMaterial, MPResourcesStandardDetail,
                         ProductAssembly, ProductDetail, ProductLabor,
                         ProductMaterial, ProductStandardDetail)


def _add_data_to_main_dict(temp, main_dict):
    """Добавляет временный словарь в основной словарь dict_material"""
    for i in temp.keys():
        if i in main_dict.keys():
            main_dict[i] += temp[i]
        else:
            main_dict[i] = temp[i]
    return main_dict


def _count_plan_labor(slug, dict_labor):
    mp = get_object_or_404(ManufacturingPlan, slug=slug)
    for mplab in MPLabor.objects.filter(mp=mp):
        temp_dict = dict.fromkeys([mplab.labor.id], mplab.time)
        _add_data_to_main_dict(temp_dict, dict_labor)


def _count_detail_material_and_labor(slug, dict_material, dict_labor):
    """Рассчитывает количество материала и трудовых затрат для детали"""
    mp = get_object_or_404(ManufacturingPlan, slug=slug)
    for mpdetail in MPDetail.objects.filter(mp=mp):  # перебираем детали в изделии
        for detmat in DetailMaterial.objects.filter(detail_id=mpdetail.detail.id):
            # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
            # материалов в детали
            count = detmat.amount * mpdetail.amount
            temp_dict = dict.fromkeys([detmat.material.id], count)
            _add_data_to_main_dict(temp_dict, dict_material)

        for detlab in DetailLabor.objects.filter(detail_id=mpdetail.detail.id):
            count = detlab.time * mpdetail.amount
            temp_dict = dict.fromkeys([detlab.labor.id], count)
            _add_data_to_main_dict(temp_dict, dict_labor)


def _count_assembly_material_standarddetail_labor(
    slug, dict_material, dict_labor, dict_stand
):
    """Рассчитывает количество материала, стандартных изделий и трудовых затрат для сборочной единицы"""
    mp = get_object_or_404(ManufacturingPlan, slug=slug)
    for assembly in MPAssembly.objects.filter(mp=mp):  # перебираем узлы в плане
        for detail in assembly.assembly.details.all():  # перебираем детали в узле
            for assemblydetail in AssemblyDetail.objects.filter(
                assembly_id=assembly.assembly.id
            ).filter(detail_id=detail.id):
                # перебираем модель отношения деталей в узле, для возможности обратиться к количеству деталей в узле
                for det in DetailMaterial.objects.filter(detail_id=detail.id):
                    # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
                    # материалов в детали
                    count = det.amount * assemblydetail.amount * assembly.amount
                    temp_dict = dict.fromkeys([det.material.id], count)
                    _add_data_to_main_dict(temp_dict, dict_material)

                for assemblydetlab in DetailLabor.objects.filter(detail_id=detail.id):
                    # перебираем трудозатраты деталей узла
                    count = (
                        assemblydetlab.time * assemblydetail.amount * assembly.amount
                    )
                    # собираем все трудозатраты в словарь, чтобы объединить работы выполняемые на одном станке
                    temp_dict = dict.fromkeys([assemblydetlab.labor.id], count)
                    _add_data_to_main_dict(temp_dict, dict_labor)

        for (
            material
        ) in assembly.assembly.materials.all():  # перебираем материалы в узле
            for assemblymaterial in AssemblyMaterial.objects.filter(
                material_id=material.id
            ).filter(assembly_id=assembly.assembly.id):
                # перебираем отношения материалов в узле
                count = assemblymaterial.amount * assembly.amount
                temp_dict = dict.fromkeys([assemblymaterial.material.id], count)
                _add_data_to_main_dict(temp_dict, dict_material)

        for (
            standetail
        ) in (
            assembly.assembly.standard_details.all()
        ):  # перебираем стандартные изделия в узле
            for assemstanddet in AssemblyStandardDetail.objects.filter(
                assembly_id=assembly.assembly.id
            ).filter(standard_detail_id=standetail.id):
                # перебираем модель отношения стандартных изделий в узле, для возможности обратиться
                # к количеству стандартных изделий в узле
                count = assemstanddet.amount * assembly.amount
                temp_dict = dict.fromkeys([assemstanddet.standard_detail.id], count)
                _add_data_to_main_dict(temp_dict, dict_stand)

        for (
            assemblylab
        ) in assembly.assembly.labors.all():  # перебираем трудовые затраты в узле
            for assemblylab_rel in AssemblyLabor.objects.filter(
                assembly_id=assembly.assembly.id
            ).filter(labor_id=assemblylab.id):
                count = assemblylab_rel.time * assembly.amount
                temp_dict = dict.fromkeys([assemblylab_rel.labor.id], count)
                _add_data_to_main_dict(temp_dict, dict_labor)


def _count_product_material_standarddetail_labor(
    slug, dict_material, dict_labor, dict_stand
):
    mp = get_object_or_404(ManufacturingPlan, slug=slug)
    for product in MPProduct.objects.filter(mp=mp):  # перебираем изделия в плане
        for assembly in ProductAssembly.objects.filter(
            product_id=product.product.id
        ):  # перебираем узлы в изделии
            for detail in assembly.assembly.details.all():  # перебираем детали в узле
                for assemblydetail in AssemblyDetail.objects.filter(
                    detail_id=detail.id
                ).filter(assembly_id=assembly.assembly.id):
                    # перебираем модель отношения деталей в узле, для возможности обратиться к количеству деталей в узле

                    for det in DetailMaterial.objects.filter(detail_id=detail.id):
                        # перебираем модель отношение материалов в деталях, для возможности обратиться к весу
                        # материалов в детали
                        count = (
                            det.amount
                            * assemblydetail.amount
                            * assembly.amount
                            * product.amount
                        )
                        # соберем словарь ключ=(id материала) значение=(количество)
                        temp_dict = dict.fromkeys([det.material.id], count)
                        _add_data_to_main_dict(temp_dict, dict_material)

                    for assemblydetlab in DetailLabor.objects.filter(
                        detail_id=detail.id
                    ):
                        # перебираем трудозатраты деталей узла
                        count = (
                            assemblydetlab.time
                            * assemblydetail.amount
                            * assembly.amount
                            * product.amount
                        )
                        # собираем все трудозатраты в словарь, чтобы объединить работы выполняемые на одном станке
                        temp_dict = dict.fromkeys([assemblydetlab.labor.id], count)
                        _add_data_to_main_dict(temp_dict, dict_labor)

                for assemblymaterial in AssemblyMaterial.objects.filter(
                    assembly_id=assembly.assembly.id
                ):
                    # перебираем отношения материалов в узле
                    count = assemblymaterial.amount * assembly.amount * product.amount
                    temp_dict = dict.fromkeys([assemblymaterial.material.id], count)
                    _add_data_to_main_dict(temp_dict, dict_material)

                for standetail in assembly.assembly.standard_details.all():
                    # перебираем стандартные изделия в узле
                    for assemstanddet in AssemblyStandardDetail.objects.filter(
                        assembly_id=assembly.assembly.id
                    ).filter(standard_detail_id=standetail.id):
                        # перебираем модель отношения стандартных изделий в узле, для возможности обратиться
                        # к количеству стандартных изделий в узле
                        count = assemstanddet.amount * assembly.amount * product.amount
                        temp_dict = dict.fromkeys(
                            [assemstanddet.standard_detail.id], count
                        )
                        _add_data_to_main_dict(temp_dict, dict_stand)

                for (
                    assemblylab
                ) in (
                    assembly.assembly.labors.all()
                ):  # перебираем трудовые затраты в узле
                    for assemblylab_rel in AssemblyLabor.objects.filter(
                        assembly_id=assembly.assembly.id
                    ).filter(labor_id=assemblylab.id):
                        count = assemblylab_rel.time * assembly.amount * product.amount
                        temp_dict = dict.fromkeys([assemblylab_rel.labor.id], count)
                        _add_data_to_main_dict(temp_dict, dict_labor)

        for productdetail in ProductDetail.objects.filter(
            product_id=product.product.id
        ):  # перебираем детали в изделии
            for detmat in DetailMaterial.objects.filter(
                detail_id=productdetail.detail.id
            ):
                # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
                # материалов в детали
                count = detmat.amount * productdetail.amount * product.amount
                temp_dict = dict.fromkeys([detmat.material.id], count)
                _add_data_to_main_dict(temp_dict, dict_material)

            for detlab in DetailLabor.objects.filter(detail_id=productdetail.detail.id):
                count = detlab.time * productdetail.amount * product.amount
                temp_dict = dict.fromkeys([detlab.labor.id], count)
                _add_data_to_main_dict(temp_dict, dict_labor)

        for prodmat in ProductMaterial.objects.filter(product_id=product.product.id):
            count = prodmat.amount * product.amount
            temp_dict = dict.fromkeys([prodmat.material.id], count)
            _add_data_to_main_dict(temp_dict, dict_material)

        for prodlab in ProductLabor.objects.filter(product_id=product.product.id):
            count = prodlab.time * product.amount
            temp_dict = dict.fromkeys([prodlab.labor.id], count)
            _add_data_to_main_dict(temp_dict, dict_labor)

        for standdet in ProductStandardDetail.objects.filter(
            product_id=product.product.id
        ):
            count = standdet.amount * product.amount
            temp_dict = dict.fromkeys([standdet.standard_detail.id], count)
            _add_data_to_main_dict(temp_dict, dict_stand)


def _get_manuf_plan_resources(slug):
    mp = get_object_or_404(ManufacturingPlan, slug=slug)
    dict_material, dict_labor, dict_stand = dict(), dict(), dict()

    _count_product_material_standarddetail_labor(
        slug, dict_material, dict_labor, dict_stand
    )
    _count_assembly_material_standarddetail_labor(
        slug, dict_material, dict_labor, dict_stand
    )
    _count_detail_material_and_labor(slug, dict_material, dict_labor)
    _count_plan_labor(slug, dict_labor)

    try:
        mpr = MPResources.objects.create(name=mp.name, slug=mp.slug)
        for key, value in dict_material.items():
            MPResourcesMaterial.objects.create(
                mp_resources_id=mpr.id, material_id=key, amount=value
            )
        for key, value in dict_labor.items():
            MPResourcesLabor.objects.create(
                mp_resources_id=mpr.id, labor_id=key, time=value
            )
        for key, value in dict_stand.items():
            MPResourcesStandardDetail.objects.create(
                mp_resources_id=mpr.id, standard_detail_id=key, amount=value
            )
    except IntegrityError:
        pass
