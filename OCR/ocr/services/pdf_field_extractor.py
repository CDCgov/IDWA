import json
import random
from typing import Dict, List, Optional, Tuple
import pypdf
import os
from pdf2image import convert_from_path


class PDFFieldExtractor:
    def __init__(self, file_path: str):
        """
        Initialize the PDF Field Extractor with a specific file path.

        Parameters:
            file_path (str): The path to the PDF file to be processed.
        """
        self.file_path = file_path
        self.reader = None
        self.writer = None
        self.form_fields = []

    def initialize_reader(self, base_path: Optional[str] = None) -> None:
        """
        Initialize the PDF reader for the specified file.

        Parameters:
            base_path (str, optional): The base path where the PDF file is located.
                                       If None, it defaults to the directory of this script.
        """
        if base_path is None:
            base_path = os.path.dirname(__file__)
        full_path = os.path.join(base_path, self.file_path)
        self.reader = pypdf.PdfReader(full_path)
        self.writer = pypdf.PdfWriter()

    def close_reader(self) -> None:
        """
        Close the PDF reader to release resources.
        """
        if self.reader is not None:
            self.reader.stream.close()
            self.reader = None

    def fill_out_pdf(self):
        self.writer.clone_reader_document_root(self.reader)

        page = self.reader.pages[0]
        fields = self.reader.get_fields()
        print(fields)

        self.writer.add_page(page)

        self.writer.update_page_form_field_values(self.writer.pages[0], {"City": "Dallas Yo!"})

        # write "output" to PyPDF2-output.pdf
        with open("filled-out.pdf", "wb") as output_stream:
            self.writer.write(output_stream)

    def list_annotations(self):
        """
         Generates a list of annotations in the pdf provided this method is mostly used for debugging purposes

        Returns:
            str: A string list of the type of annotations the name of the fields and its coordinates on the page
        """
        for page_number, page in enumerate(self.reader.pages, start=1):
            print(f"Page {page_number}:")
            annotations = page.get("/Annots")
            if annotations is None:
                print("  No annotations on this page.")
                continue
            for annot in annotations:
                if isinstance(annot, pypdf.generic.IndirectObject):
                    annot = annot.get_object()
                field_name = annot.get("/T")
                rect = annot.get("/Rect")
                subtype = annot.get("/Subtype")
                annot.set()
                print(f"Annotation - Type: {subtype}, Field Name: {field_name}, Coordinates: {rect}")

    def generate_random_color(self) -> str:
        """
        Generate a random RGB color.

        Returns:
            str: A string representing the RGB color in the format "r,g,b".
        """
        r, g, b = [random.randint(0, 255) for _ in range(3)]
        return f"{r},{g},{b}"

    def create_rectangle_annotation(self, rect: List[float], color_str: str):
        """
        Create a rectangle annotation dictionary

        Parameters:
            rect (list): The rectangle coordinates for the annotation.
            color_str (str): A string representing the RGB color in the format "r,g,b".

        Returns:
            pypdf.generic.DictionaryObject: The annotation dictionary object.
        """
        r, g, b = map(int, color_str.split(","))
        r, g, b = r / 255.0, g / 255.0, b / 255.0  # Use floating-point division
        return pypdf.generic.DictionaryObject(
            {
                pypdf.generic.NameObject("/Type"): pypdf.generic.NameObject("/Annot"),
                pypdf.generic.NameObject("/Subtype"): pypdf.generic.NameObject("/Square"),
                pypdf.generic.NameObject("/Rect"): rect,
                pypdf.generic.NameObject("/C"): pypdf.generic.ArrayObject(
                    [
                        pypdf.generic.FloatObject(r),
                        pypdf.generic.FloatObject(g),
                        pypdf.generic.FloatObject(b),
                    ]
                ),
                pypdf.generic.NameObject("/IC"): pypdf.generic.ArrayObject(
                    [
                        pypdf.generic.FloatObject(r),
                        pypdf.generic.FloatObject(g),
                        pypdf.generic.FloatObject(b),
                    ]
                ),
                pypdf.generic.NameObject("/F"): pypdf.generic.NumberObject(4),
                pypdf.generic.NameObject("/BS"): pypdf.generic.DictionaryObject(
                    {pypdf.generic.NameObject("/W"): pypdf.generic.FloatObject(0)}
                ),
            }
        )

    def update_annotations_and_save(
        self, output_path: str, pages, color_label_map: Dict[str, str]
    ) -> Tuple[str, str]:
        """
        Write modified pages to a new PDF and save the color-to-field mappings to a JSON file.

        Parameters:
            output_path (str): The path to save the modified PDF.
            pages (list): A list of page objects that have been modified.
            color_label_map (dict): A dictionary mapping RGB strings to field names.

        Returns:
            tuple: A tuple containing the paths to the saved PDF and JSON files.
        """
        output = pypdf.PdfWriter()
        for page in pages:
            output.add_page(page)
        with open(output_path, "wb") as output_stream:
            output.write(output_stream)

        # Save the color mappings
        labels_path = os.path.splitext(output_path)[0] + "_labels.json"
        with open(labels_path, "w") as json_file:
            json.dump(color_label_map, json_file, indent=4)
        return output_path, labels_path

    def mark_rectangles_on_pdf(self) -> Tuple[str, str]:
        """
        Process the PDF to add rectangle annotations and save the document along with a JSON mapping file.

        Raises:
            ValueError: If the PDF reader is not initialized.

        Returns:
            tuple: Paths to the modified PDF file and the JSON labels file.
        """
        if self.reader is None:
            raise ValueError("PDF reader is not initialized. Call initialize_reader() first.")

        color_label_map = {}
        count = 0
        for page in self.reader.pages:
            annotations = page.get("/Annots", pypdf.generic.ArrayObject())

            new_annotations = pypdf.generic.ArrayObject()
            for annot in annotations:
                if isinstance(annot, pypdf.generic.IndirectObject):
                    annot = annot.get_object()

                field = annot.get("/T") if annot.get("/T") else f"invalid_string_{random.random()}"
                rect = annot.get("/Rect")

                if field and rect:
                    color = self.generate_random_color()
                    color_str = ",".join(map(str, map(int, color.split(","))))
                    color_label_map[color_str] = field

                    new_annot = self.create_rectangle_annotation(rect, color)
                    new_annotations.append(new_annot)

                    if count < 5:
                        pdf_color = new_annot.get("/C").get_object()
                        pdf_color_values = [int(color_val * 255) for color_val in pdf_color]
                        pdf_color_str = ",".join(map(str, pdf_color_values))
                        print(f"Color in labels file: {color_str}")
                        print(f"Color in PDF annotation: {pdf_color_str}")
                        count += 1
                else:
                    new_annotations.append(annot)  # Add annotations with null fields

            page[pypdf.generic.NameObject("/Annots")] = new_annotations  # set the annotations array back to the page

        output_path = os.path.splitext(self.file_path)[0] + "_marked.pdf"
        return self.update_annotations_and_save(output_path, self.reader.pages, color_label_map)

    def pdf_to_images(self, path) -> List[str]:
        """
        Converts each page of the PDF to a PNG image file.

        Raises:
            ValueError: If the PDF reader is not initialized.

        Returns:
            List[str]: A list containing the paths to the saved image files for each page of the PDF.
        """
        if self.reader is None:
            raise ValueError("PDF reader is not initialized. Call initialize_reader() first.")

        base_path = os.path.splitext(self.file_path)[0]
        output_folder = os.path.dirname(base_path)
        os.makedirs(output_folder, exist_ok=True)

        image_paths = []
        images = convert_from_path(path, dpi=300)

        # Save each image to the defined path
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"page_{i+1}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)

        return image_paths
