from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TemplateImageRenderingTest(unittest.TestCase):
  def test_provider_images_use_https_dom_helper(self):
    base_template = (ROOT / "templates/base.html").read_text(encoding="utf-8")
    picture_template = (ROOT / "templates/picture.html").read_text(encoding="utf-8")
    stream_template = (ROOT / "templates/stream.html").read_text(encoding="utf-8")

    self.assertIn("function appendHttpsImage", base_template)
    self.assertIn('typeof source !== "string"', base_template)
    self.assertIn("/^https:\\/\\//i.test(source)", base_template)
    self.assertIn('$("<img>").addClass(className).attr("src", source)', base_template)
    self.assertIn('appendHttpsImage(".photos", "instagram", img)', picture_template)
    self.assertEqual(2, stream_template.count('appendHttpsImage(".photos", "glass",'))
    self.assertNotIn("html +=", picture_template + stream_template)

  def test_glass_tokens_are_encoded_before_url_construction(self):
    stream_template = (ROOT / "templates/stream.html").read_text(encoding="utf-8")

    self.assertIn("encodeURIComponent(val)", stream_template)
    self.assertNotIn('"/img?token=" + val', stream_template)


if __name__ == "__main__":
  unittest.main()
