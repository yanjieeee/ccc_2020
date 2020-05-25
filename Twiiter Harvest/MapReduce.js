function(doc) {
  if (doc.Place && doc.Lang == 'en')  {
        emit(doc.Place, doc.Text);
    }
    else
  if (doc.User.location && doc.Lang == 'en')  {
        emit(doc.User, doc.Text);
    }
}



    # Australia: geocode="%f,%f,%fkm" % (-26.9, 133, 2000),
    # Melbourne: geocode="%f,%f,%fkm" % (-37.840935, 144.946457, 45),
    # Sydney: geocode="%f,%f,%fkm" % (-33.865143, 151.209900, 45),
    # Brisbane: geocode="%f,%f,%fkm" % (-27.470125, 153.021072, 45),
    # Perth: geocode="%f,%f,%fkm" % (-31.953512, 115.857048, 45),
    # Adelaide: geocode="%f,%f,%fkm" % (-34.846111, 138.503052, 45),
    # Darwin: geocode="%f,%f,%fkm" % (-12.462827, 130.841782, 45),
    # Canberra: geocode="%f,%f,%fkm" % (-35.343784, 149.082977, 45),
    # Hobart: geocode="%f,%f,%fkm" % (-42.880554, 147.324997, 45),
    # Gold Coast: geocode="%f,%f,%fkm" % (-28.016666, 153.399994, 45),
    # Geelong: geocode="%f,%f,%fkm" % (-38.150002, 144.350006, 45),
    # Newcastle: geocode="%f,%f,%fkm" % (-32.916668, 151.750000, 45),
    # Wollongong: geocode="%f,%f,%fkm" % (-34.425072, 150.893143, 45),
    # Cairns: geocode="%f,%f,%fkm" % (-16.925491, 145.754120, 45),
    # Toowoomba: geocode="%f,%f,%fkm" % (-27.566668, 151.949997, 45),
    # Townsville: geocode="%f,%f,%fkm" % (-19.258965, 146.816956, 45),
    # Ballarat: geocode="%f,%f,%fkm" % (-37.549999, 143.850006, 45),
    # Bendigo: geocode="%f,%f,%fkm" % (-36.757786, 144.278702, 45),
    # Sunshine Coast: geocode="%f,%f,%fkm" % (-26.650000, 153.066666, 45),
    # Launceston: geocode="%f,%f,%fkm" % (-41.429825, 147.157135, 45),


    design_doc = {
        '_id': '_design/TestDesignDoc',
        'views': {
            'TestView': {
                'map':
                    'function(doc){if (doc.User.location){emit(doc, 1);}}'
            }
        }
    }
    db.save(design_doc)