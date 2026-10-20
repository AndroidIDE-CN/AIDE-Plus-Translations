#!/usr/bin/env python3
"""AIDE+ 翻译校验（翻译仓库的 CI 与主仓库导入共用同一份规则）。

用法：python translation_check.py <含 values/ 与 values-xx/ 的目录>
规则：XML 合法；译文的 key 必须出现在 values/ 原文中且类型相同；格式占位符（%1$s、%d 等）与原文一致；
plurals 必须含 other；string-array 条目数与原文相同；不能为空；未转义的单引号会导致 aapt 失败。
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

TAGS = ('string', 'plurals', 'string-array')
PLACEHOLDER = re.compile(r'%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[sdfxXoeEgGcb%]')
LOCALE_DIR = re.compile(r'^values-(?:[a-z]{2,3}(?:-r[A-Z]{2})?|b\+[a-z]{2,3}(?:\+[A-Z][a-z]{3})?(?:\+(?:[A-Z]{2}|[0-9]{3}))?)$')


def element_text(element):
    """元素内的完整文本（含 <xliff:g> 等子元素中的文字）"""
    return ''.join(element.itertext())


def placeholders(text):
    return sorted(p for p in PLACEHOLDER.findall(text) if p != '%%')


def unescaped_apostrophe(text):
    """aapt2 要求单引号写成 \\'（或整段放在双引号中）"""
    stripped = text.strip()
    if len(stripped) >= 2 and stripped.startswith('"') and stripped.endswith('"'):
        return False
    return re.search(r"(?<!\\)'", text) is not None


def load(path):
    """{(tag, name): element}；解析失败抛出 ET.ParseError"""
    tree = ET.parse(path)
    result = {}
    for element in tree.getroot():
        if element.tag in TAGS and element.get('name'):
            result[(element.tag, element.get('name'))] = element
    return result


def items(element):
    if element.tag == 'string':
        return {'text': element_text(element)}
    out = {}
    for index, item in enumerate(element.findall('item')):
        key = item.get('quantity') if element.tag == 'plurals' else str(index)
        out[key] = element_text(item)
    return out


def check(root):
    errors = []
    base_dir = os.path.join(root, 'values')
    if not os.path.isdir(base_dir):
        return ['missing values/ directory: ' + base_dir]
    source = {}
    for name in sorted(os.listdir(base_dir)):
        if not name.endswith('.xml'):
            continue
        try:
            for key, element in load(os.path.join(base_dir, name)).items():
                if key in source:
                    errors.append('values/%s: duplicate %s %s' % (name, key[0], key[1]))
                source[key] = element
        except ET.ParseError as e:
            errors.append('values/%s: invalid XML: %s' % (name, e))
    for qualifier in sorted(os.listdir(root)):
        directory = os.path.join(root, qualifier)
        if qualifier == 'values' or not os.path.isdir(directory) or not qualifier.startswith('values-'):
            continue
        if not LOCALE_DIR.match(qualifier):
            errors.append('%s: not a language resource directory (use values-xx, values-xx-rYY or values-b+...)' % qualifier)
            continue
        seen = set()
        for name in sorted(os.listdir(directory)):
            if not name.endswith('.xml'):
                continue
            where = '%s/%s' % (qualifier, name)
            try:
                translated = load(os.path.join(directory, name))
            except ET.ParseError as e:
                errors.append('%s: invalid XML: %s' % (where, e))
                continue
            for key, element in translated.items():
                label = '%s: %s %s' % (where, key[0], key[1])
                if key in seen:
                    errors.append(label + ': duplicate')
                seen.add(key)
                if key not in source:
                    errors.append(label + ': not in values/ (removed or misspelled key)')
                    continue
                original, target = items(source[key]), items(element)
                if key[0] == 'plurals':
                    if 'other' not in target:
                        errors.append(label + ': plurals needs quantity="other"')
                elif set(original) != set(target):
                    errors.append(label + ': %d items, values/ has %d' % (len(target), len(original)))
                for item_key, text in target.items():
                    reference = original.get(item_key, original.get('other', ''))
                    if not text.strip():
                        errors.append('%s [%s]: empty' % (label, item_key))
                    if placeholders(reference) != placeholders(text):
                        errors.append('%s [%s]: placeholders %s, values/ has %s' % (label, item_key, placeholders(text), placeholders(reference)))
                    if unescaped_apostrophe(text):
                        errors.append("%s [%s]: escape ' as \\'" % (label, item_key))
    return errors


def main(argv):
    root = argv[1] if len(argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app')
    errors = check(root)
    for error in errors:
        print(error)
    print('%d problem(s)' % len(errors))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
