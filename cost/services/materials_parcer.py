from bs4 import BeautifulSoup

from cost.models import Material


def get_materials_data():
    with open("cost/services/inf.html") as f:
        soup = BeautifulSoup(f, "html.parser")
    tr_tags = soup.find_all("div", {"class": "table-price"})
    materials_data = []
    for tr_tag in tr_tags:
        price_tags = tr_tag.find_all("div", {"class": "tr js-item-block"})
        for price_tag in price_tags:
            title_tag = price_tag.find("div", {"class": "td title"}).text.strip()
            price_char_tag = (
                price_tag.find_all("div", {"class": "td price list_char"})[1]
                .text.replace("руб.", "")
                .strip()
            )
            price_tag = (
                price_tag.find("div", {"class": "td price"})
                .text.replace("руб.", "")
                .strip()
            )
            materials_data.append((title_tag, price_char_tag, price_tag))
    return materials_data


def create_or_update_materials(materials_data):
    materials_create = []
    materials_update = []
    for title_tag, price_char_tag, price_tag in materials_data:
        material = Material.objects.filter(name=title_tag)
        if not material:
            materials_create.append(
                Material(
                    name=title_tag,
                    price_per_meter=price_char_tag,
                    price_per_ton=price_tag,
                )
            )
        elif material and hasattr(material, "price_per_ton"):
            if (
                material.price_per_ton != price_tag
                or material.price_per_meter != price_char_tag
            ):
                materials_update.append(
                    Material(
                        id=material.id,
                        name=title_tag,
                        price_per_meter=price_char_tag,
                        price_per_ton=price_tag,
                    )
                )
    if materials_create:
        Material.objects.bulk_create(materials_create)
    if materials_update:
        Material.objects.bulk_update(
            materials_update, ["name", "price_per_meter", "price_per_ton"]
        )


def parser_material():
    materials_data = get_materials_data()
    create_or_update_materials(materials_data)
    return "success"
