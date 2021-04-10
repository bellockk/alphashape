import shapefile
import pye57
import wget
import tempfile

with tempfile.TemporaryDirectory() as temp:
    filename = wget.download(
        'https://phoenixnap.dl.sourceforge.net/project/e57-3d-imgfmt/'
        'E57Example-data/Trimble_StSulpice-Cloud-50mm.e57',
        out=temp)
    e57 = pye57.E57(filename)
    data = e57.read_scan_raw(0)
    with shapefile.Writer("Trimble_StSulpice-Cloud-50mm") as w:
        w.field('name', 'C')
        w.multipointz(list(zip(
            data["cartesianX"], data["cartesianY"], data["cartesianZ"])))
        w.record(name="pointcloud")
