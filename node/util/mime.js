var _ = require('underscore')
var path = require('path')


var map = {
    'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
    'text': ['txt', 'md', ''],
    'movie': ['mkv', 'avi', 'rmvb'],
}

exports.stat= function(folder, file) {
    result = {
        name: path.basename(file, path.extname(file)),
        dir: folder,
    }
    ext = path.extname(file).substr(1)
    result.type = 'blank'
    if (!ext){
        result.type = 'folder' // change required
        result.dir=path.join(folder, file)
      }
    else {
        for (var key in map) {
            if (_.include(map[key], ext)) {
                result.type = key
                break;
            }
        }
    }
    return result
}
