import csv
from collections import OrderedDict
from asyncio import sleep, run
from typing import NamedTuple

from bs4 import BeautifulSoup
from requests import get as get_request


DATA_SPEC_FIELDS = OrderedDict({
    'Name': 'modelname',
    'photo_link': '',
    'mini_photo': '',
    'description': '',
    'brand': '',
    'barcode': '',
    'tags': '',
    'video_link': '',
    'use_first_video_as_cover': '',
    'instructions': '',
    'manufacturing_country': '',
    'manufacturer_articul': '',
    'manufacturer': '',
    'weight_with_pkg': '',
    'dimensions_with_pkg': '',
    'more_than_one_place': '',
    'price': '',
    'price_before_discount': '',
    'cost_for_seller': '',
    'additional_expenses': '',
    'currency': '',
    'valid_until': '',
    'valid_until_comment': '',
    'service_period': '',
    'service_period_comment': '',
    'warranty_period': '',
    'warranty_period_comment': '',
    'document_number': '',
    'tn_ved_code': '',
    'type_of_used_condition': '',
    'appearance': '',
    'appearance_description': '',
    'SKU_on_market': '',
    'in_archive': '',
    'type': '',
    'operating_system': 'os',
    'model_series': 'modelname',
    'body_type': '',
    'screen_diagonal': 'displaysize-hl',
    'memory_card_slot': 'memoryslot',
    'wireless_interfaces': '',
    'RAM_size': 'ramsize-hl',
    'physical_memory': 'internalmemory',
    'cpu': 'chipset',
    'main_camera_resolution_range': '',
    'connectivity_type': 'nettech',
    'screen_matrix_type': 'displaytype',
    'screen_resolution': 'displayresolution',
    'screen_refresh_frequency': '',
    'color_for_filter': 'colors',
    'SIM_count': '',
    'os_version_on_start': 'os',
    'camera_functions': '',
    'main_cameras_count': '',
    'main_camera_resolution': 'cam1modules',
    'main_cameras_type': '',
    'main_camera_specs': '',
    'main_camera_specs_2': '',
    'main_camera_specs_3': '',
    'main_camera_specs_4': '',
    'main_camera_specs_5': '',
    'max_video_resolution': 'cam1video',
    'video_main_camera': '',
    'front_camera_resolution': 'cam2modules',
    'wifi_standard': 'wlan',
    'bluetooth_version': 'bluetooth',
    'location_system': '',
    'body_material': '',
    'protection_type': 'bodyother',
    'authentication_type': 'sensors',
    'unusual_specs': '',
    'earphones_port': '',
    'weight_gr': 'weight',
    'height_mm': 'dimensions',
    'width_mm': '',
    'length_mm': '',
    'screen_resolution_format': 'displayresolution',
    'screen_ppi': '',
    'unusual_screen_specs': '',
    'additional_screen_resolution': '',
    'additional_screen_diagonal': '',
    'battery_mah': 'batdescription1',
    'battery_life_video': '',
    'battery_life_idle': '',
    'charging_time': '',
    'charger_functions': '',
    'fast_charge_standard': '',
    'charger_port_type': 'usb',
    'battery_mount': '',
    'full_package_contents': '',
    'additional_info': '',
    'announcement_date': 'year',
    'selling_start_date': 'released-hl',
    'selling_start_year': '',
    'color_name_from_manufacturer': '',
    'version': '',
    'memory_configuration': '',
    'NFC': 'nfc',
    'cpu_specs': 'cpu',
    'subscription_type': '',
    'pdp_last_edit_date': '',
    'additional_specs': '',
})


async def sleep_with_counter(seconds: int) -> None:
    for i in range(seconds, 0, -1):
        print(f'Sleeping for {i} seconds', end='\r')
        await sleep(1)


class PhoneLink(NamedTuple):
    phone_name: str
    phone_link: str


def get_phone_links() -> list[PhoneLink]:
    result: list[PhoneLink] = []
    with open('phone_links.csv', 'r') as csvfile:
        links_reader = csv.reader(csvfile, delimiter=',')
        for row in links_reader:
            phone_link = PhoneLink(*row)
            result.append(phone_link)

    return result


def get_page_text(link: str) -> str:
    return get_request(link).text


def get_page_soup(response_text: str) -> BeautifulSoup:
    return BeautifulSoup(response_text, 'html.parser')


def parse_value_from_soup(soup: BeautifulSoup, key: str) -> str:
    if key == '':
        return ''
    found_el = soup.find(attrs={'data-spec': key})
    if not found_el:
        return ''

    full_value = found_el.text
    first_value_part = full_value.split(',')[0].strip().replace('"', '')

    return first_value_part


def append_to_result(row: list[str]) -> None:
    with open('result.csv', 'a') as file:
        file.write('\t'.join(row) + '\n')


def main():
    print('Getting phone links from file')
    phone_links = get_phone_links()
    print('Starting phones parsing!')
    for name, link in phone_links:
        print(f'\n\n\nParsing data for {name}')
        csv_row: list[str] = []
        try:
            page_text = get_page_text(link)
            soup = get_page_soup(page_text)
            for key in DATA_SPEC_FIELDS.values():
                value = parse_value_from_soup(soup, key)
                csv_row.append(value)

            append_to_result(csv_row)
            run(sleep_with_counter(17))

        except Exception as e:
            print(f'Skipping {name} because of error:\n{e}')
            run(sleep_with_counter(17))
            continue



if __name__ == '__main__':
    main()
