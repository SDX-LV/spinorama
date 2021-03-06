import logging
import math
import copy
import altair as alt
from .display import \
    display_spinorama, \
    display_onaxis, \
    display_inroom, \
    display_reflection_early, \
    display_reflection_horizontal, \
    display_reflection_vertical, \
    display_spl_horizontal, \
    display_spl_vertical, \
    display_contour_horizontal, \
    display_contour_vertical, \
    display_contour_smoothed_horizontal, \
    display_contour_smoothed_vertical, \
    display_radar_horizontal, \
    display_radar_vertical


def scale_params(params, factor):
    spacing = 20
    new_params = copy.deepcopy(params)
    width = params['width']
    height = params['height']
    if factor == 3:
        new_width = math.floor(width - 6*spacing)/3
        new_height = math.floor(height /3)
    else:
        new_width = math.floor(width - 3*spacing)/2
        new_height = math.floor(height /2)
    new_params['width'] = new_width
    new_params['height'] = new_height
    for check in ('xmin', 'xmax'):
        if check not in new_params.keys():
            logging.error('scale_param {0} is not a key'.format(check))
    if new_params['xmin'] == new_params['xmax']:
            logging.error('scale_param x-range is empty')
    if 'ymin' in new_params.keys() and 'ymax' in new_params.keys() and new_params['ymin'] == new_params['ymax']:
            logging.error('scale_param y-range is empty')
    return new_params


def template_compact(df, params):
    params2 = scale_params(params, 2)
    params3 = scale_params(params, 3)
    # full size
    spinorama = display_spinorama(df, params)
    # side by side
    onaxis = display_onaxis(df, params2)
    inroom = display_inroom(df, params2)
    # side by side
    ereflex = display_reflection_early(df, params3)
    hreflex = display_reflection_horizontal(df, params3)
    vreflex = display_reflection_vertical(df, params3)
    # side by side
    hspl = display_spl_horizontal(df, params2)  
    vspl = display_spl_vertical(df, params2)
    # side by side
    hcontour = display_contour_smoothed_horizontal(df, params2)
    hradar = display_radar_horizontal(df, params2)
    # side by side
    vcontour = display_contour_smoothed_vertical(df, params2)
    vradar = display_radar_vertical(df, params2)
    # build the chart
    # print('Status {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}'.format(
    #     spinorama is None, onaxis is None, inroom is None, ereflex is None, vreflex is None, hreflex is None,
    #     hspl is None, vspl is None, hcontour is None, vcontour is None, hradar is None, vradar is None))
    chart = alt.vconcat()
    if spinorama is not None:
        chart &= alt.hconcat(spinorama.properties(title='CEA2034'))
    if onaxis is not None:
        if inroom is not None:
            chart &= alt.hconcat(onaxis.properties(title='On Axis'),
                                inroom.properties(title='In Room prediction'))
        else:
            chart &= onaxis
    if ereflex is not None and hreflex is not None and vreflex is not None:
        chart &= alt.hconcat(ereflex.properties(title='Early Reflections'),
                             hreflex.properties(title='Horizontal Reflections'),
                             vreflex.properties(title='Vertical Reflections'))
    if hspl is not None and vspl is not None:
        chart &= alt.hconcat(hspl.properties(title='Horizontal SPL'),
                             vspl.properties(title='Vertical SPL'))
    else:
        if hspl is not None:
            chart &= hspl
        elif vspl is not None:
            chart &= vspl
    if hcontour is not None and hradar is not None:
        chart &= alt.hconcat(hcontour.properties(title='Horizontal SPL'),
                             hradar.properties(title=' HorizontalSPL'))
    if vcontour is not None and vradar is not None:
        chart &= alt.hconcat(vcontour.properties(title='Vertical SPL'),
                             vradar.properties(title='Vertical SPL'))
    return chart.configure_title(
        orient='top',
        anchor='middle',
        fontSize=18
    )


def template_panorama(df, params):
    params3 = scale_params(params, 3)
    # side by side
    spinorama = display_spinorama(df, params3)
    onaxis = display_onaxis(df, params3)
    inroom = display_inroom(df, params3)
    # side by side
    ereflex = display_reflection_early(df, params3)
    hreflex = display_reflection_horizontal(df, params3)
    vreflex = display_reflection_vertical(df, params3)
    # side by side
    hspl = display_spl_horizontal(df, params3)
    hcontour = display_contour_smoothed_horizontal(df, params3)
    hradar = display_radar_horizontal(df, params3)
    # side by side
    vcontour = display_contour_smoothed_vertical(df, params3)
    vspl = display_spl_vertical(df, params3)
    vradar = display_radar_vertical(df, params3)
    # build the chart
    chart = alt.vconcat()
    if spinorama is not None and onaxis is not None and inroom is not None:
        chart &= alt.hconcat(spinorama.properties(title='CEA2034'),
                             onaxis.properties(title='On Axis'),
                             inroom.properties(title='In Room prediction'))
    else:
        if spinorama is not None:
            chart &= spinorama
        if onaxis is not None:
            chart &= onaxis
        if inroom is not None:
            chart &= inroom
    if ereflex is not None and hreflex is not None and vreflex is not None:
        chart &= alt.hconcat(ereflex.properties(title='Early Reflections'),
                             hreflex.properties(title='Horizontal Reflections'),
                             vreflex.properties(title='Vertical Reflections'))
    else:
        logging.info('Panaroma: ereflex={0} hreflex={1} vreflex={2}'.format(
            ereflex is not None, hreflex is not None, vreflex is not None))
    if hspl is not None and hcontour is not None and hradar is not None:
        chart &= alt.hconcat(hcontour.properties(title='Horizontal SPL'),
                             hradar.properties(title='Horizontal SPL'),
                             hspl.properties(title='Horizontal SPL'))
    else:
        logging.info('Panaroma: hspl={0} hcontour={1} hradar={2}'.format(
            hspl is not None, hcontour is not None, hradar is not None))
    if vspl is not None and vcontour is not None and vradar is not None:
        chart &= alt.hconcat(vcontour.properties(title='Vertical SPL'),
                             vradar.properties(title='Vertical SPL'),
                             vspl.properties(title='Vertical SPL'))
    else:
        logging.info('Panaroma: vspl={0} vcontour={1} vradar={2}'.format(
            vspl is not None, vcontour is not None, vradar is not None))
    return chart.configure_legend(
        orient='top'
    ).configure_title(
        orient='top',
        anchor='middle',
        fontSize=18
    )


def template_vertical(df, params):
    spinorama = display_spinorama(df, params)
    onaxis = display_onaxis(df, params)
    inroom = display_inroom(df, params)
    ereflex = display_reflection_early(df, params)
    hreflex = display_reflection_horizontal(df, params)
    vreflex = display_reflection_vertical(df, params)
    hspl = display_spl_horizontal(df, params)
    vspl = display_spl_vertical(df, params)
    hcontour = display_contour_horizontal(df, params)
    hradar = display_radar_horizontal(df, params)
    vcontour = display_contour_vertical(df, params)
    vradar = display_radar_vertical(df, params)
    chart = alt.vconcat()
    for g in (spinorama, onaxis, inroom, ereflex, hreflex, vreflex,
              hspl, vspl, hcontour, hradar, vcontour, vradar):
        if g is not None:
            chart &= g
    return chart.configure_legend(
        orient='top'
    ).configure_title(
        orient='top',
        anchor='middle',
        fontSize=18
    )


# def template_freq_sidebyside(s1, s2, name, width=450, height=450):
#     df1 = display_graph_freq(s1[name], params)
#     df2 = display_graph_freq(s2[name], params)
#     if df1 is None and df2 is None:
#         return None
#     if df1 is None:
#         return df2
#     if df2 is None:
#         return df1
#     return alt.hconcat(df1, df2)
