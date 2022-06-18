from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from cost.models import Product, ProductDetail, ProductStandardDetail, Detail, DetailLabor, ProductLabor, \
    ProductAssembly, Assembly, AssemblyDetail, AssemblyLabor, AssemblyStandardDetail, DetailMaterial, ProductMaterial, \
    ManufacturingPlan, MPResources, MPResourcesMaterial, MPResourcesLabor, MPResourcesStandardDetail, MPProduct, \
    MPAssembly, MPLabor, MPDetail, Material, AssemblyMaterial


def _add_material_to_dict_material(temp_dict, dict_material):
    """Добавляет материал в словарь dict_material"""
    for i in temp_dict.keys():
        if i in dict_material.keys():
            dict_material[i] += temp_dict[i]
        else:
            dict_material[i] = temp_dict[i]
    return dict_material


def _add_standard_detail_to_dict_stand(temp_dict, dict_stand):
    """Добавляет стандартное изделие в словарь dict_stand"""
    for i in temp_dict.keys():
        if i in dict_stand.keys():
            dict_stand[i] += temp_dict[i]
        else:
            dict_stand[i] = temp_dict[i]
    return dict_stand


def _add_labor_to_dict_labor(temp_dict, dict_labor):
    """Добавляет трудовые затраты в словарь dict_labor"""
    for i in temp_dict.keys():
        if i in dict_labor.keys():
            dict_labor[i] += temp_dict[i]
        else:
            dict_labor[i] = temp_dict[i]
    return dict_labor


def _get_manuf_plan_resources(slug):
    mp = get_object_or_404(ManufacturingPlan, slug=slug)
    dict_material = dict()
    dict_labor = dict()
    dict_stand = dict()
    for product in MPProduct.objects.filter(mp=mp):  # перебираем изделия в плане

        for assembly in ProductAssembly.objects.filter(product_id=product.product.id):  # перебираем узлы в изделии

            for detail in assembly.assembly.details.all():  # перебираем детали в узле

                for assemblydetail in AssemblyDetail.objects.filter(detail_id=detail.id).filter(
                        assembly_id=assembly.assembly.id):
                    # перебираем модель отношения деталей в узле, для возможности обратиться к количеству деталей в узле
                    for det in DetailMaterial.objects.filter(detail_id=detail.id):

                    # перебираем модель отношение материалов в деталях, для возможности обратиться к весу
                    # материалов в детали
                                        
                        count = det.amount * assemblydetail.amount * assembly.amount * product.amount
                        # print(det.material.name + ' - ' + str(assemblydetail.amount)
                        #       + ' * ' + str(det.amount)
                        #       + ' * ' + str(assembly.amount)
                        #       + ' * ' + str(assembly.amount)
                        #       + ' = ' + str(count))

                        # соберем словарь ключ=(id материала) значение=(количество)
                        temp_dict = dict.fromkeys([det.material.id], count)
                        _add_material_to_dict_material(temp_dict, dict_material)

                    
                    for assemblydetlab in DetailLabor.objects.filter(detail_id=detail.id):
                        # перебираем трудозатраты деталей узла
                        count = assemblydetlab.time * assemblydetail.amount * assembly.amount * product.amount
                        # print(detail.name + ' - ' + str(assemblydetlab.labor.id) + ' - ' + assemblydetlab.labor.name
                        #       + ' - ' + assemblydetlab.labor.machine + ' - ' + str(assemblydetlab.time)
                        #       + ' * ' + str(assemblydetail.amount)
                        #       + ' * ' + str(assembly.amount)
                        #       + ' * ' + str(product.amount)
                        #       + ' = ' + str(count))
                        # собираем все трудозатраты в словарь, чтобы объединить работы выполняемые на одном станке
                        temp_dict = dict.fromkeys([assemblydetlab.labor.id], count)
                        _add_labor_to_dict_labor(temp_dict, dict_labor)

                for assemblymaterial in AssemblyMaterial.objects.filter(assembly_id=assembly.assembly.id):
                    # перебираем отношения материалов в узле

                    count = assemblymaterial.amount * assembly.amount * product.amount
                    temp_dict = dict.fromkeys([assemblymaterial.material.id], count)
                    _add_material_to_dict_material(temp_dict, dict_material)


            for standetail in assembly.assembly.standard_details.all():
                # перебираем стандартные изделия в узле
                # asd = AssemblyStandardDetail.objects.filter(standard_detail_id=standetail.id)
                for assemstanddet in AssemblyStandardDetail.objects.filter(assembly_id=assembly.assembly.id).filter(
                        standard_detail_id=standetail.id):
                    # перебираем модель отношения стандартных изделий в узле, для возможности обратиться
                    # к количеству стандартных изделий в узле
                    count = assemstanddet.amount * assembly.amount * product.amount
                    # print(assemstanddet.standard_detail.name + ' - ' + str(assemstanddet.amount)
                    #       + ' * ' + str(assemstanddet.amount)
                    #       + ' * ' + str(assembly.amount)
                    #       + ' * ' + str(product.amount)
                    #       + ' = ' + str(count))
                    temp_dict = dict.fromkeys([assemstanddet.standard_detail.id], count)
                    _add_standard_detail_to_dict_stand(temp_dict, dict_stand)

        for productdetail in ProductDetail.objects.filter(product_id=product.product.id):
            # print(productdetail)
            # перебираем детали в изделии
            # print(productdetail.detail.name + ' - ' + str(productdetail.amount))
            for detmat in DetailMaterial.objects.filter(detail_id=productdetail.detail.id):
                # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
                # материалов в детали
                count = detmat.amount * productdetail.amount * product.amount
                # print(productdetail.detail.name + ' - ' + detmat.material.name + ' - ' + str(productdetail.amount) +
                #       ' * ' + str(detmat.amount) + ' = ' + str(count))
                temp_dict = dict.fromkeys([detmat.material.id], count)
                _add_material_to_dict_material(temp_dict, dict_material)

            for detlab in DetailLabor.objects.filter(detail_id=productdetail.detail.id):
                count = detlab.time * productdetail.amount * product.amount
                # print(str(detlab.labor.id) + ' - ' + detlab.labor.name + ' - ' + detlab.labor.machine
                #       + ' - ' + str(detlab.time) + ' - ' + str(count))
                temp_dict = dict.fromkeys([detlab.labor.id], count)
                _add_labor_to_dict_labor(temp_dict, dict_labor)

        for prodmat in ProductMaterial.objects.filter(product_id=product.product.id):
            count = prodmat.amount * product.amount
            temp_dict = dict.fromkeys([prodmat.material.id], count)
            _add_material_to_dict_material(temp_dict, dict_material)

        for prodlab in ProductLabor.objects.filter(product_id=product.product.id):
            # print(prodmat.material.name + ' - ' + str(prodmat.amount))
            # print(prodlab.time)
            # print(product.amount)
            count = prodlab.time * product.amount
            temp_dict = dict.fromkeys([prodlab.labor.id], count)
            _add_labor_to_dict_labor(temp_dict, dict_labor)

        for standdet in ProductStandardDetail.objects.filter(product_id=product.product.id):
            # print(standdet.standard_detail.name + ' - ' + str(standdet.amount))
            count = standdet.amount * product.amount
            temp_dict = dict.fromkeys([standdet.standard_detail.id], count)
            _add_standard_detail_to_dict_stand(temp_dict, dict_stand)

    for assembly in MPAssembly.objects.filter(mp=mp):
        # перебираем узлы в плане
        for detail in assembly.assembly.details.all():
            # перебираем детали в узле
            # ad1 = AssemblyDetail.objects.filter(detail_id=detail.id)
            # print(ad1)
            for assemblydetail in AssemblyDetail.objects.filter(assembly_id=assembly.assembly.id).filter(
                    detail_id=detail.id):
                # перебираем модель отношения деталей в узле, для возможности обратиться к количеству деталей в узле
                for det in DetailMaterial.objects.filter(detail_id=detail.id):
                    # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
                    # материалов в детали
                    count = det.amount * assemblydetail.amount * assembly.amount
                    # соберем словарь ключ=(id материала) значение=(количество)
                    temp_dict = dict.fromkeys([det.material.id], count)
                    _add_material_to_dict_material(temp_dict, dict_material)

                for assemblydetlab in DetailLabor.objects.filter(detail_id=detail.id):
                    # перебираем трудозатраты деталей узла
                    count = assemblydetlab.time * assemblydetail.amount * assembly.amount
                    # print(detail.name + ' - ' + str(assemblydetlab.labor.id) + ' - ' + assemblydetlab.labor.name
                    #       + ' - ' + assemblydetlab.labor.machine + ' - ' + str(assemblydetlab.time)
                    #       + ' * ' + str(assemblydetail.amount) + ' * ' + str(assembly.amount) + ' = ' +
                    #       str(count))
                    # собираем все трудозатраты в словарь, чтобы объединить работы выполняемые на одном станке
                    temp_dict = dict.fromkeys([assemblydetlab.labor.id], count)
                    _add_labor_to_dict_labor(temp_dict, dict_labor)

        for material in assembly.assembly.materials.all():
            # print(material)
            # print(assembly.assembly.materials.all())
            # перебираем материалы в узле
            # print(AssemblyMaterial.objects.filter(material_id=material.id, assembly_id=assembly.id))
            # am1 = AssemblyMaterial.objects.filter(material_id=material.id)
            for assemblymaterial in AssemblyMaterial.objects.filter(material_id=material.id).filter(
                    assembly_id=assembly.assembly.id):
                # print(assemblymaterial.material)
                # print(assemblymaterial.amount)
                # перебираем отношения материалов в узле
                count = assemblymaterial.amount * assembly.amount
                temp_dict = dict.fromkeys([assemblymaterial.material.id], count)
                _add_material_to_dict_material(temp_dict, dict_material)

        for standetail in assembly.assembly.standard_details.all():
            # перебираем стандартные изделия в узле
            # asd1 = AssemblyStandardDetail.objects.filter(standard_detail_id=standetail.id)
            for assemstanddet in AssemblyStandardDetail.objects.filter(assembly_id=assembly.assembly.id).filter(
                    standard_detail_id=standetail.id):
                # перебираем модель отношения стандартных изделий в узле, для возможности обратиться
                # к количеству стандартных изделий в узле
                count = assemstanddet.amount * assembly.amount
                # print(assemstanddet.standard_detail.name + ' - ' + str(assemstanddet.amount)
                #       + ' * ' + str(assemstanddet.amount)
                #       + ' * ' + str(assembly.amount)
                #       + ' * ' + str(product.amount)
                #       + ' = ' + str(count))
                temp_dict = dict.fromkeys([assemstanddet.standard_detail.id], count)
                _add_standard_detail_to_dict_stand(temp_dict, dict_stand)

    for mpdetail in MPDetail.objects.filter(mp=mp):
        # перебираем детали в изделии
        # print(productdetail.detail.name + ' - ' + str(productdetail.amount))
        for detmat in DetailMaterial.objects.filter(detail_id=mpdetail.detail.id):
            # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
            # материалов в детали
            count = detmat.amount * mpdetail.amount
            # print(productdetail.detail.name + ' - ' + detmat.material.name + ' - ' + str(productdetail.amount) +
            #       ' * ' + str(detmat.amount) + ' = ' + str(count))
            temp_dict = dict.fromkeys([detmat.material.id], count)
            _add_material_to_dict_material(temp_dict, dict_material)

        for detlab in DetailLabor.objects.filter(detail_id=mpdetail.detail.id):
            count = detlab.time * mpdetail.amount
            # print(str(detlab.labor.id) + ' - ' + detlab.labor.name + ' - ' + detlab.labor.machine
            #       + ' - ' + str(detlab.time) + ' - ' + str(count))
            temp_dict = dict.fromkeys([detlab.labor.id], count)
            _add_labor_to_dict_labor(temp_dict, dict_labor)

    for mplab in MPLabor.objects.filter(mp=mp):
        temp_dict = dict.fromkeys([mplab.labor.id], mplab.time)
        _add_labor_to_dict_labor(temp_dict, dict_labor)

    try:
        mpr = MPResources.objects.create(name=mp.name, slug=mp.slug)
        for key, value in dict_material.items():
            MPResourcesMaterial.objects.create(
                mp_resources_id=mpr.id, material_id=key, amount=value)
        for key, value in dict_labor.items():
            MPResourcesLabor.objects.create(
                mp_resources_id=mpr.id, labor_id=key, time=value)
        for key, value in dict_stand.items():
            MPResourcesStandardDetail.objects.create(
                mp_resources_id=mpr.id, standard_detail_id=key, amount=value)
    except IntegrityError:
       pass
