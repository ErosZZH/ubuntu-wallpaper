import argparse
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    path = args.path
    if not os.path.isdir(path):
        raise FileNotFoundError('Invalid path')
    return args.path

def scan_images(path: str) -> list[str]:
    imgs = []
    for r, d, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                imgs.append(os.path.join(r, file))
    return imgs

def generate_xml(imgs: list[str]) -> str:
    img_str = ''
    template = '''
  <static>
    <duration>1795.0</duration>
    <file>{0}</file>
  </static>
  <transition>
    <duration>5.0</duration>
    <from>{0}</from>
    <to>{1}</to>
  </transition>
'''
    for i in range(len(imgs)):
        img_str += template.format(imgs[i], imgs[(i+1)%len(imgs)])
    xml ='''<background>
  <starttime>
    <year>2009</year>
    <month>08</month>
    <day>04</day>
    <hour>00</hour>
    <minute>00</minute>
    <second>00</second>
  </starttime>
  {0}
</background>
'''
    return xml.format(img_str)

def update_xml(source: str, target: str) -> None:
    with open(target, 'w') as f:
        f.write(source)

if __name__ == '__main__':
    target_file = '/usr/share/backgrounds/contest/jammy.xml'
    path = get_args()
    imgs = scan_images(path)
    xml = generate_xml(imgs)
    update_xml(xml, target_file)
    print('Done')