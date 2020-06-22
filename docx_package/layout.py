# TODO: comment
#####     LAYOUT DEFINITION     #####

# Some functions that define the layout and formatting of the report are implemented in this module.
# It includes: document layout, header, footer, styles, tables, ...
from docx.text.paragraph import Paragraph
from docx.table import _Row, _Column, _Cell
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.shared import Pt, Cm, RGBColor
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import nsdecls, qn
from docx.oxml import parse_xml
from docx.oxml.shared import OxmlElement


class Layout:
    """
    Class that represents and defines the layout and formatting of the report.
    """

    # TODO: use this
    # define some colors
    BLACK = RGBColor(0, 0, 0)  # Hex: 000000
    BLACK_35 = RGBColor(90, 90, 90)  # Hex: 5A5A5A
    LIGHT_GREY_10 = RGBColor(208, 206, 206)  # Hex: D0CECE

    def __init__(self, document):
        self.document = document

    # define the page setup of as section as default A4 setup
    def define_page_format(self, section):
        section.orientation = WD_ORIENT.PORTRAIT  # orientation of the page: portrait
        section.page_width = Cm(21)  # page width: 21 cm
        section.page_height = Cm(29.7)  # page height: 29,7 cm
        section.top_margin = Cm(2.5)  # top margin: 2,5 cm
        section.bottom_margin = Cm(2.5)  # bottom margin: 2,5 cm
        section.right_margin = Cm(2.5)  # right margin: 2,5 cm
        section.left_margin = Cm(2.5)  # left margin: 2,5 cm

    def define_style(self, name, font, size, color, alignment, italic, bold):
        """
        Define the characteristics of a style in a document.

        Args:
            name: Name of the style that is defined.
            font: Font name
            size: Font size
            color: Font color
            alignment: Alignment of the paragraph (left, right, center, justify).
            italic: Boolean to know if it should be italic.
            bold: Boolean to know if it should be bold.
        """

        # add a new style if it does not already exist
        if name not in self.document.styles:
            self.document.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)

        style = self.document.styles[name]

        # this let us modify the font of some styles that are kind of "blocked"
        try:
            style.element.xpath('w:rPr/w:rFonts')[0].attrib.clear()
        except IndexError:
            pass

        style.font.name = font
        style.font.size = Pt(size)
        style.font.color.rgb = color
        style.paragraph_format.alignment = alignment
        style.font.italic = italic
        style.font.bold = bold

    @ classmethod
    def define_all_styles(cls, document):
        """
        Define all relevant styles of a document.

        Args:
            document: .docx file whose styles will be defined.
        """

        layout = cls(document)

        layout.define_style('Title', 'Calibri Light', 32, black, WD_ALIGN_PARAGRAPH.CENTER, False, False)
        layout.define_style('Subtitle', 'Calibri Light', 24, black_35, WD_ALIGN_PARAGRAPH.CENTER, False, False)
        layout.define_style('Heading 1', 'Calibri', 16, black, WD_ALIGN_PARAGRAPH.LEFT, False, True)
        layout.define_style('Heading 2', 'Calibri Light', 14, black, WD_ALIGN_PARAGRAPH.LEFT, False, True)
        layout.define_style('Heading 3', 'Calibri Light', 12, black, WD_ALIGN_PARAGRAPH.LEFT, False, True)
        layout.define_style('Normal', 'Calibri', 11, black, WD_ALIGN_PARAGRAPH.JUSTIFY, False, False)
        # layout.define_style('Table', 'Calibri', 11, black, WD_ALIGN_PARAGRAPH.LEFT, False, False)
        layout.define_style('Picture', 'Calibri', 11, black, WD_ALIGN_PARAGRAPH.CENTER, False, False)
        layout.define_style('Caption', 'Calibri', 9, black, WD_ALIGN_PARAGRAPH.CENTER, False, True)

    def capitalize_first_letter(self, string: str) -> str:
        """
        Args:
            string: String whose first letter must be capitalized.

        Returns:
            String with a capital first letter.
        """

        return string[:1].upper() + string[1:]

    def set_cell_shading(self, cell: _Cell, color_hex: str):
        """
        Color a cell.

        Args:
            cell: Cell that must be colored.
            color_hex: Hexadecimal representation of the color.
        """

        shading_elm = parse_xml(r'<w:shd {0} w:fill="{1}"/>'.format(nsdecls('w'), color_hex))
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def insert_horizontal_border(self, paragraph: Paragraph):
        """
        Add an horizontal border under a paragraph.

        Args:
            paragraph: Paragraph under which you want to add an horizontal border.
        """

        p = paragraph._p  # p is the <w:p> XML element
        pPr = p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        pPr.insert_element_before(pBdr,
                                  'w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap',
                                  'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN',
                                  'w:bidi', 'w:adjustRightInd', 'w:snapToGrid', 'w:spacing', 'w:ind',
                                  'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap', 'w:jc',
                                  'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap',
                                  'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr',
                                  'w:pPrChange'
                                  )
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), 'auto')
        pBdr.append(bottom)

    def set_row_height(self, row: _Row, height: float, rule=WD_ROW_HEIGHT_RULE.EXACTLY):
        """
        Set the height of a table row.

        Args:
            row: Row whose height is to be changed.
            height: Height of the column in cm.
            rule (optional): Rule for determining the height of a table row, e.g. rule=WD_ROW_HEIGHT_RULE.AT_LEAST.
        """

        row.height_rule = rule
        row.height = Cm(height)

    def set_column_width(self, column: _Column, width: float):
        """
        Set the width of a table column.

        Note:
            To make it work, the autofit of the corresponding table must be disabled beforehand (table.autofit = False).

        Args:
            column: Column whose width is to be changed.
            width: Width of the column in cm.
        """

        for cell in column.cells:
            cell.width = Cm(width)

    def set_cell_border(self, cell: _Cell, **kwargs):
        """
        Set the border of a cell.

        Usage example:
        set_cell_border(cell,
                        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},     # top border
                        bottom={"sz": 12, "color": "#00FF00", "val": "single"},     # bottom border
                        start={"sz": 24, "val": "dashed", "shadow": "true"},     # left border
                        end={"sz": 12, "val": "dashed"}     # right border
                        )

        Available attributes can be found here: http://officeopenxml.com/WPtableBorders.php

        Args:
            cell: Cell with borders to be changed.
        """

        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()

        # check for tag existence, if none found, then create one
        tcBorders = tcPr.first_child_found_in("w:tcBorders")
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
            tcPr.append(tcBorders)

        # list over all available tags
        for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
            edge_data = kwargs.get(edge)
            if edge_data:
                tag = 'w:{}'.format(edge)

                # check for tag existence, if none found, then create one
                element = tcBorders.find(qn(tag))
                if element is None:
                    element = OxmlElement(tag)
                    tcBorders.append(element)

                # looks like order of attributes is important
                for key in ["sz", "val", "color", "space", "shadow"]:
                    if key in edge_data:
                        element.set(qn('w:{}'.format(key)), str(edge_data[key]))












# define some colors
black = RGBColor(0, 0, 0)                  # Hex: 000000
black_35 = RGBColor(90, 90, 90)            # Hex: 5A5A5A
light_grey_10 = RGBColor(208, 206, 206)    # Hex: D0CECE


# define the page setup of as section as default A4 setup
def define_page_format(section):
    section.orientation = WD_ORIENT.PORTRAIT   # orientation of the page: portrait
    section.page_width = Cm(21)                # page width: 21 cm
    section.page_height = Cm(29.7)             # page height: 29,7 cm
    section.top_margin = Cm(2.5)               # top margin: 2,5 cm
    section.bottom_margin = Cm(2.5)            # bottom margin: 2,5 cm
    section.right_margin = Cm(2.5)             # right margin: 2,5 cm
    section.left_margin = Cm(2.5)              # left margin: 2,5 cm


# define the characteristics of a style of a document
def define_style(document, name, font, size, color, alignment, italic, bold):

    if name in document.styles:
        print(name)

    style = document.styles[name]                                   # name of the style you want to define
    try:
        style.element.xpath('w:rPr/w:rFonts')[0].attrib.clear()     # this let us modify the font of some styles that are kind of "blocked"
    except IndexError:                                              # pass the styles for which this does not work
        pass
    style.font.name = font                                          # font name
    style.font.size = Pt(size)                                      # font size (in pt)
    style.font.color.rgb = color                                    # font color
    style.paragraph_format.alignment = alignment                    # alignment of the paragraph (left, right, center, justify)
    style.font.italic = italic                                      # boolean to know if it should be written in italic
    style.font.bold = bold                                          # boolean to know if it should be written in bold


# define all styles used in a document using the function style_definition
def define_all_styles(document):
    # document.styles.add_style('Table', WD_STYLE_TYPE.PARAGRAPH)     # add style 'Table' for the tables entries
    document.styles.add_style('Picture', WD_STYLE_TYPE.PARAGRAPH)

    define_style(document, 'Title', 'Calibri Light', 32, black, WD_ALIGN_PARAGRAPH.CENTER, False, False)
    define_style(document, 'Subtitle', 'Calibri Light', 24, black_35, WD_ALIGN_PARAGRAPH.CENTER, False, False)
    define_style(document, 'Heading 1', 'Calibri', 16, black, WD_ALIGN_PARAGRAPH.LEFT, False, True)
    define_style(document, 'Heading 2', 'Calibri Light', 14, black, WD_ALIGN_PARAGRAPH.LEFT, False, True)
    define_style(document, 'Heading 3', 'Calibri Light', 12, black, WD_ALIGN_PARAGRAPH.LEFT, False, True)
    define_style(document, 'Normal', 'Calibri', 11, black, WD_ALIGN_PARAGRAPH.JUSTIFY, False, False)
    # define_style(document, 'Table', 'Calibri', 11, black, WD_ALIGN_PARAGRAPH.LEFT, False, False)
    define_style(document, 'Picture', 'Calibri', 11, black, WD_ALIGN_PARAGRAPH.CENTER, False, False)
    define_style(document, 'Caption', 'Calibri', 9, black, WD_ALIGN_PARAGRAPH.CENTER, False, True)


def capitalize_first_letter(string: str) -> str:
    """
    Args:
        string: String whose first letter must be capitalized.

    Returns:
        String with a capital first letter.
    """

    return string[:1].upper() + string[1:]


def set_cell_shading(cell: _Cell, color_hex: str):
    """
    Color a cell.

    Args:
        cell: Cell that must be colored.
        color_hex: Hexadecimal representation of the color.
    """

    shading_elm = parse_xml(r'<w:shd {0} w:fill="{1}"/>'.format(nsdecls('w'), color_hex))
    cell._tc.get_or_add_tcPr().append(shading_elm)


def insert_horizontal_border(paragraph: Paragraph):
    """
    Add an horizontal border under a paragraph.

    Args:
        paragraph: Paragraph under which you want to add an horizontal border.
    """

    p = paragraph._p                    # p is the <w:p> XML element
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    pPr.insert_element_before(pBdr,
                              'w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap',
                              'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN',
                              'w:bidi', 'w:adjustRightInd', 'w:snapToGrid', 'w:spacing', 'w:ind',
                              'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap', 'w:jc',
                              'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap',
                              'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr',
                              'w:pPrChange'
                              )
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'auto')
    pBdr.append(bottom)


def set_row_height(row: _Row, height: float, rule=WD_ROW_HEIGHT_RULE.EXACTLY):
    """
    Set the height of a table row.

    Args:
        row: Row whose height is to be changed.
        height: Height of the column in cm.
        rule (optional): Rule for determining the height of a table row, e.g. rule=WD_ROW_HEIGHT_RULE.AT_LEAST.
    """

    row.height_rule = rule
    row.height = Cm(height)


def set_column_width(column: _Column, width: float):
    """
    Set the width of a table column.

    Note:
        To make it work, the autofit of the corresponding table must be disabled beforehand (table.autofit = False).

    Args:
        column: Column whose width is to be changed.
        width: Width of the column in cm.
    """

    for cell in column.cells:
        cell.width = Cm(width)


def set_cell_border(cell: _Cell, **kwargs):
    """
    Set the border of a cell.

    Usage example:
    set_cell_border(cell,
                    top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},     # top border
                    bottom={"sz": 12, "color": "#00FF00", "val": "single"},     # bottom border
                    start={"sz": 24, "val": "dashed", "shadow": "true"},     # left border
                    end={"sz": 12, "val": "dashed"}     # right border
                    )

    Available attributes can be found here: http://officeopenxml.com/WPtableBorders.php

    Args:
        cell: Cell with borders to be changed.
    """

    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    # check for tag existence, if none found, then create one
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)

    # list over all available tags
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)

            # check for tag existence, if none found, then create one
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))
