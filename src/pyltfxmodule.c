/******************************************************************************\
|
| Copyright (c) 2009 Novell, Inc.
| All Rights Reserved.
|
| This program is free software; you can redistribute it and/or
| modify it under the terms of version 2 of the GNU General Public License 
| as published by the Free Software Foundation.
|
| This program is distributed in the hope that it will be useful,
| but WITHOUT ANY WARRANTY; without even the implied warranty of
| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
| GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License
| along with this program; if not, contact Novell, Inc.
|
| To contact Novell about this file by physical or electronic mail,
| you may find current contact information at www.novell.com
|
\******************************************************************************/

#include "pyltfxmodule.h"
 
/*
start module functions
*/
 
PyMODINIT_FUNC
init_pyltfx( void ) 
{
    PyObject* m;
    XWindowType.tp_new = PyType_GenericNew; 
    if (PyType_Ready(&XWindowType) < 0)
        return;

    XDisplayType.tp_new = PyType_GenericNew; 
    if (PyType_Ready(&XDisplayType) < 0)
        return;

    m = Py_InitModule("_pyltfx", _pyltfx_methods);

    PyltfxError = PyErr_NewException( "_pyltfx.Error", NULL, NULL );
    Py_INCREF( PyltfxError );
    PyModule_AddObject(m, "error", PyltfxError);

    PyltfxInvalid = PyErr_NewException( "_pyltfx.InvalidError", NULL, NULL );
    Py_INCREF( PyltfxInvalid );
    PyModule_AddObject( m, "invalid", PyltfxInvalid );

    PyltfxNotFocused = PyErr_NewException( "_pyltfx.NotFocusedError", NULL, NULL );
    Py_INCREF( PyltfxNotFocused );
    PyModule_AddObject( m, "not_focused", PyltfxNotFocused );

    Py_INCREF(&XWindowType);
    PyModule_AddObject( m, "XWindow", (PyObject *)&XWindowType );
   
    Py_INCREF(&XDisplayType);
    PyModule_AddObject( m, "XDisplay", (PyObject *)&XDisplayType );

    PyModule_AddIntConstant( m, "event_empty", XWIN_EMPTY );
    PyModule_AddIntConstant( m, "event_new", XWIN_NEW );
    PyModule_AddIntConstant( m, "event_destroyed", XWIN_DESTROYED ); 
    PyModule_AddIntConstant( m, "event_mouse", XWIN_MOUSE_EVENT );
    PyModule_AddIntConstant( m, "event_keypress", XWIN_KEYPRESS_EVENT );
    PyModule_AddIntConstant( m, "event_keyrelease", XWIN_KEYRELEASE_EVENT );
    PyModule_AddIntConstant( m, "event_other", XWIN_OTHER_EVENT );
    PyModule_AddIntConstant( m, "event_except_destroyed", ALL_EXCEPT_DESTROYED );
    PyModule_AddIntConstant( m, "event_all", ALL_EVENTS );

    key_tab = PyString_FromFormat( "%c", 1 );
    PyModule_AddObject( m, "key_tab", key_tab );
    
    key_shift = PyString_FromFormat( "%c", 2 );
    PyModule_AddObject( m, "key_shift", key_shift );
    
    key_ctrl = PyString_FromFormat( "%c", 3 );
    PyModule_AddObject( m, "key_ctrl", key_ctrl );
    
    key_alt = PyString_FromFormat( "%c", 4 );
    PyModule_AddObject( m, "key_alt", key_alt );
    
    key_del = PyString_FromFormat( "%c", 5 );
    PyModule_AddObject( m, "key_del", key_del );
    
    key_bksp = PyString_FromFormat( "%c", 6 );
    PyModule_AddObject( m, "key_bksp", key_bksp );
    
    key_rtrn = PyString_FromFormat( "%c", 7 );
    PyModule_AddObject( m, "key_rtrn", key_rtrn );
    
    key_enter = PyString_FromFormat( "%c", 8 );
    PyModule_AddObject( m, "key_enter", key_enter );
    
    key_f1 = PyString_FromFormat( "%c", 9 );
    PyModule_AddObject( m, "key_f1", key_f1 );
    
    key_f2 = PyString_FromFormat( "%c", 10 );
    PyModule_AddObject( m, "key_f2", key_f2 );
    
    key_f3 = PyString_FromFormat( "%c", 11 );
    PyModule_AddObject( m, "key_f3", key_f3 );
    
    key_f4 = PyString_FromFormat( "%c", 12 );
    PyModule_AddObject( m, "key_f4", key_f4 );
    
    key_f5 = PyString_FromFormat( "%c", 13 );
    PyModule_AddObject( m, "key_f5", key_f5 );
    
    key_f6 = PyString_FromFormat( "%c", 14 );
    PyModule_AddObject( m, "key_f6", key_f6 );
    
    key_f7 = PyString_FromFormat( "%c", 15 );
    PyModule_AddObject( m, "key_f7", key_f7 );
    
    key_f8 = PyString_FromFormat( "%c", 16 );
    PyModule_AddObject( m, "key_f8", key_f8 );
    
    key_f9 = PyString_FromFormat( "%c", 17 );
    PyModule_AddObject( m, "key_f9", key_f9 );
    
    key_f10 = PyString_FromFormat( "%c", 18 );
    PyModule_AddObject( m, "key_f10", key_f10 );
    
    key_f11 = PyString_FromFormat( "%c", 19 );
    PyModule_AddObject( m, "key_f11", key_f11 );
    
    key_f12 = PyString_FromFormat( "%c", 20 );
    PyModule_AddObject( m, "key_f12", key_f12 );
    
    key_up = PyString_FromFormat( "%c", 21 );
    PyModule_AddObject( m, "key_up", key_up );
    
    key_down = PyString_FromFormat( "%c", 22 );
    PyModule_AddObject( m, "key_down", key_down );
    
    key_left = PyString_FromFormat( "%c", 23 );
    PyModule_AddObject( m, "key_left", key_left );
    
    key_right = PyString_FromFormat( "%c", 24 );
    PyModule_AddObject( m, "key_right", key_right );
    
    key_esc = PyString_FromFormat( "%c", 25 );
    PyModule_AddObject( m, "key_esc", key_esc );
    
    key_space = PyString_FromFormat( "%c", 26 );
    PyModule_AddObject( m, "key_space", key_space );
    
    key_home = PyString_FromFormat( "%c", 27 );
    PyModule_AddObject( m, "key_home", key_home );
    
    key_end = PyString_FromFormat( "%c", 28 );
    PyModule_AddObject( m, "key_end", key_end );
    
    key_pgup = PyString_FromFormat( "%c", 29 );
    PyModule_AddObject( m, "key_pgup", key_pgup );
    
    key_pgdown = PyString_FromFormat( "%c", 30 );
    PyModule_AddObject( m, "key_pgdown", key_pgdown );
}
 
static gchar *
getWindowProperty( Display *disp, Window win, /*{{{*/
               Atom xa_prop_type, gchar *prop_name, unsigned long *size) 
{
    Atom xa_prop_name;
    Atom xa_ret_type;
    int ret_format;
    unsigned long ret_nitems;
    unsigned long ret_bytes_after;
    unsigned long tmp_size;
    unsigned char *ret_prop;
    gchar *ret;
    
    xa_prop_name = XInternAtom(disp, prop_name, False);
    
    /* MAX_PROPERTY_VALUE_LEN / 4 explanation (XGetWindowProperty manpage):
     *
     * long_length = Specifies the length in 32-bit multiples of the
     *               data to be retrieved.
     */
    if (XGetWindowProperty(disp, win, xa_prop_name, 0, MAX_PROPERTY_VALUE_LEN / 4, False,
            xa_prop_type, &xa_ret_type, &ret_format,     
            &ret_nitems, &ret_bytes_after, &ret_prop) != Success) {
        TRACEF((stderr, "Cannot get %s property.\n", prop_name))
        return NULL;
    }
  
    if (xa_ret_type != xa_prop_type) {
        TRACEF((stderr, "Invalid type of %s property.\n", prop_name))
        XFree(ret_prop);
        return NULL;
    }

    /* null terminate the result to make string handling easier */
    tmp_size = (ret_format / 8) * ret_nitems;
    ret = g_malloc(tmp_size + 1);
    memcpy(ret, ret_prop, tmp_size);
    ret[tmp_size] = '\0';

    if (size) {
        *size = tmp_size;
    }
    
    XFree(ret_prop);
    return ret;
}

static PyObject *
getWindowTitle (Display *display, Window window) 
{
    PyObject *title;
    unsigned long size = 0;
    gchar *name;
    XTextProperty name_return;
    int ret_code = 0;
    TRACEF_TITLE((stderr, "getWindowTitle(), for window: 0x%x\n", 
                  (unsigned int)window))

    /* FIXME work for UTF8 support
    gchar *net_wm_name;
    char *errors;
    net_wm_name = getWindowProperty(display, window, 
            XInternAtom(display, "UTF8_STRING", False), "_NET_WM_NAME", NULL);

    if (net_wm_name) 
    {
        TRACEF((stderr,"name UTF8_STRING: '%s' for window 0x%x\n", 
                net_wm_name, (unsigned int)window))
        //title = PyString_FromString(net_wm_name);
        title = PyUnicode_DecodeUTF8(net_wm_name, sizeof(net_wm_name), errors);
        //title = PyUnicode_FromWideChar((wchar_t *)net_wm_name, sizeof((wchar_t *)net_wm_name));
    }
    else 
    {
        name = getWindowProperty(display, window, XA_STRING, "WM_NAME", NULL);
        //fprintf(stderr, "name: %s, ", name);
        if (name) 
        {
            TRACEF((stderr,"name XA_STRING: '%s' for window 0x%x\n", 
                    name, (unsigned int)window))
            title = PyString_FromString(name);
            //name = g_locale_to_utf8(name, -1, NULL, NULL, NULL);
            //title = PyUnicode_FromWideChar((wchar_t *)name, sizeof((wchar_t *)name));
        }
    }
    name = getWindowProperty(display, window, XA_STRING, "WM_NAME", NULL);
    g_free(net_wm_name);
    */
    name = getWindowProperty(display, window, XA_STRING, "WM_NAME", &size);
    if (name) 
    {
        TRACEF_TITLE((stderr, "getWindowTitle(), name XA_STRING: '%s' window 0x%x\n", 
                name, (unsigned int)window)) 
        title = PyString_FromStringAndSize(name, size);
    }
    else 
    {
        ret_code = XGetWMName(display, window,  &name_return);
        if( ret_code != 0 )
        {
            TRACEF_TITLE((stderr,"getWindowTitle(), XGetWMName name_return: '%s' for window 0x%x\n", 
                    name_return.value, (unsigned int)window))
            title = PyString_FromString(name_return.value);
        }
        else
        {
            TRACEF_TITLE((stderr, "getWindowTitle(), returning None"))
            Py_INCREF(Py_None);
            title = Py_None;
        }
    }
    g_free(name);
    return  title;
}

static PyObject *
XWindow_getTitle( XWindow *self )
{
    PyObject *result PyNone;
    TRACEF_TITLE((stderr, "getTitle(), for window: 0x%x\n",  
                    (unsigned int)self->this_window))
    /*
    if( isValidXWindow( self ) )
    {
        TRACEF_TITLE((stderr, "getTitle(), isValidXWindow() True\n"))
        if( self->window_title == Py_None )
        {
            TRACEF_TITLE((stderr, "getTitle(), self->window_title == Py_None \n"))
            result = getWindowTitle( self->this_display, self->this_window );
        }
        else
        {
            TRACEF_TITLE((stderr, "getTitle(), self->window_title != Py_None\n"))
            Py_INCREF( self->window_title );
            result = self->window_title;
        }
    }
    else
    {
        TRACEF_TITLE((stderr, "getTitle(), isValidXWindow() False\n"))
        if( self->window_title == Py_None ) 
        {
            result = PyString_FromString( "" );
        }
        else
        {
            Py_INCREF(self->window_title);
            result = self->window_title;
        }
        //Py_INCREF(Py_None);
        //result = Py_None;
    }
    */
    if( isValidXWindow( self ) )
    {
        TRACEF_TITLE((stderr, "getTitle(), self->window_title == Py_None \n"))
        result = getWindowTitle( self->this_display, self->this_window );
    }
    if( result == PyNone )
    {
        if( self->window_title == Py_None )
        {
            result = PyString_FromString( "" )
        }
        else
        {
            result = self->window_title
            Py_INCREF( result )
        }
    }
    return result;
}

static PyObject *
createXWindow( Window window, 
               Display *display, 
               XEvent *event, 
               int no_title )
{
    XWindowAttributes war;
    int ret_code = 0;
    XWindow* result = NULL;

    TRACEF((stderr,"window parameter: 0x%x\n",  (unsigned int)window))
    TRACEF((stderr,"display parameter: %p\n", display))
    TRACEF((stderr,"event: 0x%x\n", (unsigned int)event))
    /* We are going to test to see if the returned window has a title
    set, if it does, we will return it. otherwise, we will continue
    and check the revert_return values, We have to do this because of
    the different places the toolkits keep their info. */
    result = (XWindow *) XWindow_new( &XWindowType, 
                                      (PyObject *)NULL, 
                                      (PyObject *)NULL );
    if ( result == NULL )
    {
        TRACEF_NEW_WIN((stderr,"ERROR creating XWindow object"))
        PyErr_SetString( PyltfxError, "Could not create XWindow object" );
        return NULL;
    }
    result->this_display = display;
    result->this_window = window;
    result->event_type = XWIN_EMPTY;
    if( window == 0 )
    {
        TRACEF_NEW_WIN((stderr,"window is null"))
        return (PyObject *) result;
    } 
    
    if( event == NULL )
    {
        result->event_type = XWIN_NEW;
    }
    else
    {
        TRACEF_NEW_WIN((stderr, "event->type: %i, xiwindow:0x%x\n", event->type, (unsigned int)window))
        switch( event->type )
        {
            case CreateNotify:
            {
                result->event_type = XWIN_NEW;
            }
            break;
            
            case DestroyNotify:
            case UnmapNotify:
            {
                result->event_type = XWIN_DESTROYED;
                TRACEF_NEW_WIN((stderr,"Destroyed window: 0x%x\n",  (unsigned int)window))
            }
            break;
            
            case KeyPress: 
            {
                result->event_type = XWIN_KEYPRESS_EVENT;
                TRACEF_NEW_WIN((stderr,"KeyPress: 0x%x\n",  (unsigned int)window))
            }
            break;
            
            case KeyRelease:
            {
                result->event_type = XWIN_KEYRELEASE_EVENT;
                TRACEF_NEW_WIN((stderr,"KeyRelease: 0x%x\n",  (unsigned int)window))
            }
            break;
            
            default:
            {
                result->event_type = XWIN_OTHER_EVENT;
                TRACEF_NEW_WIN((stderr,"Other event: 0x%x\n",  (unsigned int)window))
            }
            break;
        }
    }
    if( ((result->event_type != XWIN_DESTROYED) ||
         (result->event_type != XWIN_NEW)) && 
        (no_title == FALSE) )    
    {
        //TRACEF_NEW_WIN((stderr,"window before getWindow: 0x%x\n", (unsigned int)window))
        window = getWindow( window, display ); 
        //TRACEF_NEW_WIN((stderr,"window after getWindow: 0x%x\n", (unsigned int)window))
        result->this_window = window;
    }
    
    if( result->event_type != XWIN_DESTROYED ) 
    {
        ret_code = XGetWindowAttributes(display, window, &war);
        if( ret_code != 0 )
        {
            if( ((result->event_type == XWIN_NEW) || (war.class == InputOutput)) ) 
            {
                result->window_title = getWindowTitle( display, window );
           }
           else
           {
               TRACEF_NEW_WIN((stderr,"Window 0x%x not InputOutput\n",  (unsigned int)window))
               TRACEF_NEW_WIN((stderr,"war.class: %i, InputOutput: %i\n", war.class, InputOutput))
           }
       }
       else
       {
           TRACEF_NEW_WIN((stderr,"ERROR getting window attributes: %i\n", ret_code))
       }
   } /* DESTROYED_WINDOW */
   TRACEF_NEW_WIN((stderr,"this_window: 0x%x\n this_display: %p\n parent_window: 0x%x\n event_type: %i\n",
          (unsigned int)result->this_window, result->this_display, 
          (unsigned int)result->parent_window, result->event_type))
   fprintf(stderr, "\n ***** createXWindow 0x%x\n event_type: %i\n XEvent: 0x%x\n", result->this_window, result->event_type, (unsigned int)event);
   return (PyObject *) result;
}

static Window
getWindow( Window window, Display *display )
{
    int ret_code = 0;
    int revert_return;
    XTextProperty title_return;
    Window focus_return;
    Window parent_return = 0;
    Window root_return;
    Window *children_return;
    unsigned int nchildren_return;
    TRACEF((stderr,"getWindow(), window 0x%x\n",  (unsigned int)window))
    TRACEF((stderr,"getWindow(), display %p\n", display))
  
    /*
    ret_code=XGetWindowAttributes(display, target, &window_attributes_return);
    XGetInputFocus( display, &window, &revert_return );
    ret_code = XFetchName( display, window, &title_return );
    */
    ret_code = XGetWMName( display, window,  &title_return );
    if( ret_code != 0 )
    {
        TRACEF((stderr,"title_return: %s for 0x%x\n", title_return.value, (unsigned int)window))
        /*FIXME needed ? XFree(title_return);*/
    }
    else 
    {
        XGetInputFocus( display, &focus_return, &revert_return );
        if( focus_return == window )
        {
            if( revert_return == RevertToParent )
            {
                ret_code = XQueryTree(display, window, &root_return,
                        &parent_return, &children_return,
                        &nchildren_return);
                if( ret_code != 0 )
                {
                    window = parent_return;
                }
            }
        }
        else
        {
            TRACEF((stderr,"XGetInputFocus, window 0x%x does not match focus_return: 0x%x\n",  (unsigned int)window, (unsigned int)focus_return))
        }
    }
    /*else
        window has no title and we're not reverting to parent
        FIXME what about the panel?
       return (Window)result;
    */
    TRACEF((stderr,"return window: 0x%x\n",  (unsigned int)window))
    return window;
}


static int
isFocusXWindow( XWindow *xwindow )
{
    int result = FALSE;
    Window top;
    if( isValidXWindow( xwindow ) ) 
    {
      top = getActiveWindow( xwindow->this_display );
      if( xwindow->this_window == top )
      {
          result = TRUE;
      }
    }
    return result;
}

static int
isValidXWindow( XWindow *xwindow )
{
    int ret_code;
    int result = TRUE;
    XWindowAttributes war;

    if( xwindow == NULL )
    {
        result = FALSE;
        TRACEF((stderr,"xwindow is NULL"))
    }
    else if( (xwindow->this_window == 0) || (xwindow->this_display == NULL) )
    {
        result = FALSE;
        TRACEF((stderr,"xwindow->this_window is 0 or xwindow->this_display is NULL"))
    }
    else if( (xwindow->event_type == XWIN_DESTROYED) || 
             (xwindow->event_type == XWIN_EMPTY) )
    {
        result = FALSE;
        TRACEF((stderr,"XWIN_DESTROYED or XWIN_EMPTY for window: 0x%x\n",
               (unsigned int) xwindow->this_window))
    }
    else
    {
        ret_code = XGetWindowAttributes( xwindow->this_display, 
                                         xwindow->this_window, 
                                         &war);
        if( (ret_code == 0) || (war.map_state != IsViewable) || 
            (war.class != InputOutput) )
        {
            result = FALSE;
            TRACEF((stderr,"XGetWindowAttributes failed for window 0x%x\n ret_code: %i\n war.map_state (IsUnmapped: 0, IsUnviewable: 1, IsViewable: 2): %i\n war.class: %i\n",
                   (unsigned int) xwindow->this_window,
                   ret_code,
                   war.map_state,
                   war.class))
        }
        else
        {
            int len_prop_array;
            Atom *props;
            props = XListProperties( xwindow->this_display,
                                     xwindow->this_window,
                                     &len_prop_array);
            if( props == NULL)
            {
                result = FALSE;
                TRACEF((stderr,"XListProperties failed for window 0x%x\n", 
                        (unsigned int)xwindow->this_window))
            }
            else
            {
                XFree(props);
            }

            if( xwindow->window_title == Py_None )
            {
                result = FALSE;
                TRACEF((stderr,"No title for window: 0x%x\n", 
                       (unsigned int) xwindow->this_window))
            }
        }
    }
    return result;  
}
/*
end module functions
*/

/*
start xwindow
*/
static PyObject *
XWindow_new( PyTypeObject *type, PyObject *args, PyObject *kwds )
{
    XWindow *self = NULL;
    struct timeval tv;

    self = (XWindow *)type->tp_alloc(type, 0);
    if( self != NULL ) 
    {
        self->key_state = 0;
        if( gettimeofday(&tv, NULL) == 0 )
        {
            self->timestamp = tv.tv_sec + (double)tv.tv_usec / 1000000;
        } else {
            /* FIXME error */
            self->timestamp = 0;
        }
        self->event_type = XWIN_EMPTY;
        self->this_window = 0;
        self->parent_window = 0;
        self->is_window_manager = 0;
        self->this_display = NULL;
        Py_INCREF(Py_None);
        self->window_title = Py_None;
        Py_INCREF( Py_None );
        self->key_chars = Py_None;
        Py_INCREF( Py_None );
        self->window_manager = Py_None;
    }
    return (PyObject *)self;
}

static int
XWindow_init(XWindow *self, PyObject *args, PyObject *kwds)
{
    PyObject *title=NULL;
    static char *kwlist[] = {"title", NULL};
    if(! PyArg_ParseTupleAndKeywords(args, kwds, "|O", kwlist, &title ))
        return -1;

    return 0;
}

static void
XWindow_dealloc( XWindow *self )
{
    Py_DECREF( self->window_title );
    Py_DECREF( self->key_chars );
    self->ob_type->tp_free( (PyObject*)self );
    //PyObject_DEL( self );
}

static PyObject *
XWindow_repr( XWindow *self )
{
    PyObject *result;
    char *s;
    if( asprintf( &s, "<XWindow: 0x%x>", (unsigned int)self->this_window ) == -1 )
    {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate string");
        result = NULL;
    }
    else
    {
        result = PyString_FromString( s );
    }
    free( s );
    return result;
}

static long 
XWindow_hash( XWindow *self )
{
    PyObject *win_id;
    /* FIXME for platforms where Window is not a long 
#ifdef LONG64
    win_id = PyLong_FromLong( (long)self->this_window );
*/
    win_id = PyInt_FromLong( self->this_window );
/* #else
    win_id = PyLong_FromUnsignedLong( self->this_window );
#endif
*/ 
    return PyObject_Hash( win_id );

}
static int 
XWindow_cmp( XWindow *self, XWindow *other )
{ 
    int result;
    if( self->this_window == other->this_window )
    {
        result = 0;
    }
    else if( self->this_window == 0 )
    {
        result = -1;
    }
    else
    {
        result = 1;
    }
    return result;
}

static int
SendEvent( XKeyEvent *event )
{
    XSync( event->display, FALSE );
    XSetErrorHandler( ErrorHandler );
    
    TRACEF_KYBD((stderr,"XSendEvent, key code: %i, key_state: %i\n", 
                 event->keycode, event->state))
    XSendEvent( event->display, (Window)event->window, TRUE, KeyPressMask, (XEvent*)event );

    /*
    PyErr_SetString( PyltfxNotFocused, "Not current focused X window");
    return 1;
    */
    return 0;
}

static PyObject *
XWindow_type( XWindow* self, PyObject *args )
{
    const char *raw_key;
    XKeyEvent sendkey = { 0 };
    KeyCode keycode = NoSymbol; 
    long index = 0;
    Window top = 0;
    KeySym sym;
    KeySym lower;
    KeySym upper;
    char key[2];
    if (!PyArg_ParseTuple(args, "s", &raw_key))
        return NULL;
    
    TRACEF_KYBD((stderr,"raw_key as string: %s\n", raw_key))
    TRACEF_KYBD((stderr,"raw_key[0] as int: %i\n", raw_key[0]))
    key[0] = raw_key[0];
    key[1] = '\0';
    TRACEF_KYBD((stderr,"key as string: %s\n", key))
    TRACEF_KYBD((stderr,"key[0] as int: %i\n", key[0]))
    sym = XStringToKeysym(key);
    XConvertCase(sym, &lower, &upper);
    
    if( isalpha(raw_key[0]) )
    {
        TRACE_KYBD
        if( isupper(*key) )
        {
            /*
            if( sendkey.state == 0 )
            {
                sendkey.state |= (ShiftMask|AnyModifier);
            }
            */
            self->key_state |= (ShiftMask|AnyModifier);
        }
        /*
        else
        {
          sendkey.state = AnyModifier;
        }
        */
        keycode = XKeysymToKeycode(self->this_display, (KeySym)sym);
    }
    else 
    {
        index = raw_key[0];
        //if( index != 0 && index < 32 )
        if ((index >= 0) && (index < sizeof(keyindex) / sizeof(KeySym)))
        {
            TRACEF_KYBD((stderr,"index: %i\n", (int)index))
            switch( keyindex[index] )
            {
            case XK_Shift_L:
                self->key_state |= (ShiftMask);
            break;
            case XK_Alt_L:
                self->key_state |= (Mod1Mask);
            break;
            case XK_Control_L:
                self->key_state |= (ControlMask);
            break;
            case XK_Meta_L:
                /* FIXME handle 'windows' key */
            break;
            default:
                TRACEF_KYBD((stderr, "keyindex[index]: %i\n", keyindex[index]))
                keycode = XKeysymToKeycode( self->this_display, 
                                            keyindex[index] );
            break;
            break;
            }
        }
        else
        {
            TRACEF_KYBD((stderr,"Special chars switch(), raw_key: %s\n", raw_key))
            switch(*raw_key)  
            /* Everything below this is a BIG
               switch statment for special chars. */
            {                      
            case '.':
                keycode = XKeysymToKeycode(self->this_display, XK_period);
            break;
            case ' ':
                keycode = XKeysymToKeycode(self->this_display, XK_space);
            break;
            case '!':
                keycode = XKeysymToKeycode(self->this_display, XK_exclam);
                self->key_state |= (ShiftMask);
            break;
            case '@':
                keycode = XKeysymToKeycode(self->this_display, XK_at);
                self->key_state |= (ShiftMask);
            break;
            case '#':
                keycode = XKeysymToKeycode(self->this_display, XK_numbersign);
                self->key_state |= (ShiftMask);
            break;
            case '$':
                keycode = XKeysymToKeycode(self->this_display, XK_dollar);
                self->key_state |= (ShiftMask);
            break;
            case '%':
                keycode = XKeysymToKeycode(self->this_display, XK_percent);
                self->key_state |= (ShiftMask);
            break;
            case '^': 
                keycode = XKeysymToKeycode(self->this_display, XK_asciicircum);
                self->key_state |= (ShiftMask);
            break;
            case '&':
                keycode = XKeysymToKeycode(self->this_display, XK_ampersand);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case '*':
                keycode = XKeysymToKeycode(self->this_display, XK_asterisk);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case '(':
                keycode = XKeysymToKeycode(self->this_display, XK_parenleft);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case ')':
                keycode = XKeysymToKeycode(self->this_display, XK_parenright);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case ',':
                keycode = XKeysymToKeycode(self->this_display, XK_comma);
            break;
            case '-':
                keycode = XKeysymToKeycode(self->this_display, XK_minus);
            break;
            case '\\':
                keycode = XKeysymToKeycode(self->this_display, XK_backslash);
            break;
            case '/':
                keycode = XKeysymToKeycode(self->this_display, XK_slash);
            break;
            case '_':
                keycode = XKeysymToKeycode(self->this_display, XK_underscore);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case '`':
                keycode = XKeysymToKeycode(self->this_display, XK_grave);
            break;
            case '~':
                keycode = XKeysymToKeycode(self->this_display, XK_asciitilde);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case '=':
                keycode = XKeysymToKeycode(self->this_display, XK_equal);
            break;
            case '+':
                keycode = XKeysymToKeycode(self->this_display, XK_plus);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case ':':
                keycode = XKeysymToKeycode(self->this_display, XK_colon);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case ';':
                keycode = XKeysymToKeycode(self->this_display, XK_semicolon);                     
            break;
            case '0':
                keycode = XKeysymToKeycode(self->this_display, XK_0);
            break;
            case '1':
                keycode = XKeysymToKeycode(self->this_display, XK_1);
            break;
            case '2':
                keycode = XKeysymToKeycode(self->this_display, XK_2);
            break;
            case '3':
                keycode = XKeysymToKeycode(self->this_display, XK_3);
            break;
            case '4':
                keycode = XKeysymToKeycode(self->this_display, XK_4);
            break;
            case '5':
                keycode = XKeysymToKeycode(self->this_display, XK_5);
            break;
            case '6':
                keycode = XKeysymToKeycode(self->this_display, XK_6);
            break;
            case '7':
                keycode = XKeysymToKeycode(self->this_display, XK_7);
            break;
            case '8':
                keycode = XKeysymToKeycode(self->this_display, XK_8);
            break;
            case '9':
                keycode = XKeysymToKeycode(self->this_display, XK_9);
            break;
            case '[':
                keycode = XKeysymToKeycode(self->this_display, XK_bracketleft);
            break;
            case ']':
                keycode = XKeysymToKeycode(self->this_display, XK_bracketright);
            break;
            case '{':
                keycode = XKeysymToKeycode(self->this_display, XK_braceleft);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case '}':
                keycode = XKeysymToKeycode(self->this_display, XK_braceright);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case '"':
                keycode = XKeysymToKeycode(self->this_display, XK_quotedbl);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case '\'':
                keycode = XKeysymToKeycode(self->this_display, XK_apostrophe);
            break;
            case '>':
                keycode = XKeysymToKeycode(self->this_display, XK_less);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            /* for some reason these still send a > character to the window
            case '<':
                keycode = XKeysymToKeycode(self->this_display, XK_greater);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            case '|':
                keycode = XKeysymToKeycode(self->this_display, XK_brokenbar);
                self->key_state |= (ShiftMask|AnyModifier);
            break;
            */
            case '?':
                keycode = XKeysymToKeycode(self->this_display, XK_question);
                self->key_state |= (ShiftMask|AnyModifier);
            break;

                /* default: 
                sendkey.keycode = XKeysymToKeycode(display, (KeySym)sy                        continue;
                */
            }
        }
    }

    //sendkey.state |= (KeyPressMask|KeyReleaseMask);
    //XAllowEvents(self->this_display, AsyncBoth, CurrentTime);

    //sendkey.type=2;
    top = getActiveWindow( self->this_display );
    //top = getActiveWindow(self->this_display);
    if( !isValidXWindow( self ) && !self->is_window_manager )
    {
        TRACEF_KYBD((stderr,"Not a valid window: 0x%x\n",  (unsigned int)sendkey.window))
        PyErr_SetString( PyltfxInvalid, "Not a valid X window");
        return NULL;
    }
    /*
    else if( sendkey.window != top )
    {
        TRACEF((stderr,"Top window is 0x%x, not this window 0x%x\n",  (unsigned int)top, (unsigned int)sendkey.window))
        PyErr_SetString( PyltfxNotFocused, "Not current focused X window");
        return NULL;
    }
    */
    /*
    else if( self->key_state != 0 )
    {
        TRACEF((stderr, "Alt, Ctrl or shift key: %i\n", self->key_state ))
    }
    */
    if( keycode != NoSymbol )
    {
        //sendkey.state = 0;
        TRACEF_KYBD((stderr,"keycode != XK_VoidSymbol\n"))
        sendkey.type = KeyPress;
        sendkey.send_event = False;
        sendkey.display = self->this_display;
        sendkey.window = self->this_window;
        sendkey.root = DefaultRootWindow( self->this_display );
        sendkey.subwindow = None;
        sendkey.x = 1;
        sendkey.y = 1;
        sendkey.x_root = 1;
        sendkey.y_root = 1;
        sendkey.same_screen = TRUE;
        sendkey.time = CurrentTime;
        if( self->key_state & ShiftMask ) 
        {
            sendkey.keycode = XKeysymToKeycode( self->this_display, XK_Shift_L );
            SendEvent( &sendkey );
            sendkey.state |= (ShiftMask|AnyModifier);
        }
        if( self->key_state & Mod1Mask ) 
        {
            sendkey.keycode = XKeysymToKeycode( self->this_display, XK_Alt_L );
            SendEvent( &sendkey );
            sendkey.state |= (Mod1Mask|AnyModifier);
        }
        if( self->key_state & ControlMask ) 
        {
            sendkey.keycode = XKeysymToKeycode( self->this_display, XK_Control_L );
            SendEvent( &sendkey );
            sendkey.state |= (ControlMask|AnyModifier);
        }
        sendkey.keycode = keycode;
        SendEvent( &sendkey );
        /* simulate key bounce */
        usleep( 50000 );
        sendkey.type = KeyRelease;
        /* ESC key closes window on key down */
        if( self->key_state & ShiftMask )
        {
            sendkey.keycode = XKeysymToKeycode( self->this_display, XK_Shift_L );
            SendEvent( &sendkey );
            sendkey.state &= ~(ShiftMask);
        }
        if( self->key_state & Mod1Mask ) 
        {
            sendkey.keycode = XKeysymToKeycode( self->this_display, XK_Alt_L );
            SendEvent( &sendkey );
            sendkey.state &= ~(Mod1Mask|AnyModifier);
        }
        if( self->key_state & (ControlMask|AnyModifier)) 
        {
            sendkey.keycode = XKeysymToKeycode( self->this_display, XK_Control_L );
            SendEvent( &sendkey );
            sendkey.state &= ~(ControlMask|AnyModifier);
        }
        TRACEF_KYBD((stderr,"SendEvent key up\n"))
        sendkey.keycode = keycode;
        SendEvent( &sendkey );
        /*else
        {
            TRACEF_KYBD((stderr,"Key release not a valid window: 0x%x\n",  (unsigned int)sendkey.window))
        }*/
        self->key_state = 0;
        /*
        FIXME add error checking to above code.
        if( self->key_state == 0 )
        {
            sendkey.type = KeyRelease;
            TRACEF((stderr,"XSendEvent, KeyRelease: %i\n", sendkey.keycode))
            XSendEvent(self->this_display, (Window)sendkey.window, TRUE, 
                       sendkey.state, (XEvent*)&sendkey);     
            for( i=0; i<NUM_MOD_KEYS; i++ )
            {
                if( self->mod_key_state[i].window != 0 )
                {
                    TRACEF((stderr,"XSendEvent, KeyRelease: %i\n", 
                            self->mod_key_state[i].keycode))
                    self->mod_key_state[i].type = KeyRelease;
                    self->mod_key_state[i].time = CurrentTime;

                    XSendEvent( self->this_display, 
                                (Window)self->mod_key_state[i].window, 
                                TRUE, 
                                (Window)self->mod_key_state[i].state, 
                                (XEvent*)&(self->mod_key_state[i]) );     
                    self->mod_key_state[i].window = 0;
                }
            }
            //sendkey.type = KeyPress;
        }
        else
        {
            for( i=0; i<NUM_MOD_KEYS; i++ )
            {
                if( self->mod_key_state[i].display == 0 )
                {
                    self->mod_key_state[i] = sendkey;
                    break;
                }
            }
        }
        */
        XSync(self->this_display, False);
    }
    
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject * 
XWindow_activate( XWindow *self )
{
    PyObject *result;
    XWindowAttributes old;
    XSetWindowAttributes new;
    int ret_code = 0;
    TRACEF((stderr,"self->this_window: 0x%x\n",  (unsigned int)self->this_window ))
    if( !isValidXWindow( self ) )
    {
        TRACEF((stderr,"isValidXWindow returned false for: 0x%x\n",  (unsigned int)self->this_window))
        PyErr_SetString( PyltfxInvalid, "Not a valid X window");
        return NULL;
    }
    ret_code = XGetWindowAttributes(self->this_display, self->this_window, &old);
    if( ret_code != 0 )
    {
        TRACE
        if( old.override_redirect == True )
        {
            TRACE
            new.override_redirect = False;
            XChangeWindowAttributes(self->this_display, self->this_window, CWOverrideRedirect, &new);
        }
        XSetInputFocus( self->this_display, self->this_window, RevertToParent, CurrentTime);
        XRaiseWindow( self->this_display, self->this_window );
        XFlush( self->this_display );
        if (old.override_redirect == True)
        {
           TRACE
           new.override_redirect = True;
           XChangeWindowAttributes(self->this_display, self->this_window, CWOverrideRedirect, &new);         
        }
    }
    result = Py_BuildValue("i", 0);
    return result;  
}
/*
end xwindow
*/




/* 
start xdisplay
*/

/*
static PyObject *
XDisplay_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
   XDisplay *self;

   self = (XDisplay *)type->tp_alloc(type, 0);
   
   return (PyObject *)self;
}
*/

static int
XDisplay_init( XDisplay *self, PyObject *args, PyObject *kwds )
{
    self->display = NULL;
    self->root_window = 0;
    self->display_string = NULL;
    self->root_xwindow = NULL;
    self->xdisplay_string = NULL;
    self->event_callback = NULL;
 
    PyObject *xdisplay_string = NULL;

    static char *kwlist[] = {"display_string", NULL};
    if( ! PyArg_ParseTupleAndKeywords( args, kwds, "|O", kwlist, 
                                       &xdisplay_string ) )
    {
        PyErr_SetString( PyltfxError, "Error parsing arguments" );
        return -1;
    }

    if( (xdisplay_string == NULL) || 
        (PyObject_Compare( Py_None, xdisplay_string ) == 0) )
    {
        TRACEF((stderr, "Getting value of DISPLAY environment variable"))
        self->xdisplay_char = getenv("DISPLAY");
        if( self->xdisplay_char == NULL ) 
        {
            TRACEF((stderr, "DISPLAY not set defaulting to :0"))
            self->xdisplay_char = ":0";
        }
        self->xdisplay_string = PyString_FromString( self->xdisplay_char );
    }
    else
    {
        PyObject *tmp;
        TRACE
        self->xdisplay_char = PyString_AsString( xdisplay_string );
        if( self->xdisplay_char == NULL )
        {
            PyErr_SetString( PyltfxError, "Error parsing display string" );
            return -1;
        }
        tmp = self->xdisplay_string;
        Py_INCREF( xdisplay_string );
        self->xdisplay_string = xdisplay_string;
        if( tmp != NULL )
        {
            Py_DECREF(tmp);
        }
    }
    TRACEF((stderr, "xdisplay_string: %s\n", self->xdisplay_char ))
    XInitThreads();

    self->display = XOpenDisplay( self->xdisplay_char );
    if( self->display == NULL ) 
    {
        PyErr_SetString( PyltfxError, "Could not open display" );
        return -1;
    }
    self->root_window = DefaultRootWindow( self->display );
    self->root_xwindow = createXWindow( self->root_window, self->display, 
                                        NULL, TRUE );
    if( self->root_xwindow == NULL )
    {
        PyErr_SetString( PyltfxError, "Could not create root_xwindow" );
        return -1;
    }
    XSetErrorHandler( ErrorHandler );
    XSelectInput( self->display, self->root_window, EVENT_MASK );
    return 0;
}

static void
XDisplay_dealloc(XDisplay *self)
{
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject *
XDisplay_setXEventCallback(XDisplay *self, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O:setEventCallback", &temp)) {
        if (!PyCallable_Check(temp)) {
            TRACEF((stderr,"ERROR parameter is not callable\n"))
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        TRACEF((stderr,"Setting self->event_callback\n"))
        Py_XINCREF(temp);         /* Add a reference to new callback */
        Py_XDECREF(self->event_callback);  /* Dispose of previous callback */
        self->event_callback = temp;       /* Remember new callback */
        /* Boilerplate to return "None" */
        Py_INCREF(Py_None);
        result = Py_None;
    }
    return result;
}
  
static PyListObject *
XDisplay_checkXEvent( XDisplay *self )
{
    XEvent event;
    Window root;
    PyObject *result = NULL;
    PyObject *tmp_xwin = NULL;
    root = DefaultRootWindow( self->display );

    /* FIXME future with callback */
    result = PyList_New(0);
    while( XPending( self->display ) )
    {
        XNextEvent( self->display, &event );
        fprintf(stderr, "\n ***** checkXEvent 0x%x\n XEvent: %i\n", (unsigned int)event.xany.window, (unsigned int)event.type);
        switch( event.type )
        {
            case Expose:
            {
                TRACEF_NEW_WIN((stderr,"Expose window: 0x%x \n",  
                       (unsigned int)event.xexpose.window))
            }
            case CreateNotify:
            {
                TRACEF_NEW_WIN((stderr,"CreateNotify window: 0x%x parent: 0x%x\n",  
                    (unsigned int)event.xcreatewindow.window,
                    (unsigned int)event.xcreatewindow.parent))

            }/*case CreateNotify */
            case MapNotify:
            {
                TRACEF_NEW_WIN((stderr,"MapNotify window: 0x%x, event window: 0x%x\n",  
                       (unsigned int)event.xunmap.window,
                       (unsigned int)event.xunmap.event))
            }
            XSelectInput( self->display, event.xcreatewindow.window, EVENT_MASK );
  
            case DestroyNotify: 
            {
                TRACEF_NEW_WIN((stderr,"DestroyNotify window: 0x%x, event window: 0x%x\n",  
                       (unsigned int)event.xdestroywindow.window,
                       (unsigned int)event.xdestroywindow.event))
            }
            tmp_xwin = createXWindow( event.xany.window,
                                        self->display,
                                        &event,
                                        FALSE );
            if( tmp_xwin != NULL )
            {
                PyList_Append( (PyObject *)result, tmp_xwin );
            }
            else
            {
                TRACEF_NEW_WIN((stderr,"Failed to create XWindow for: 0x%x\n",  
                        (unsigned int)event.xany.window))
                /* FIXME raise python exception here? */
            }

            break;
            

            case PropertyNotify:
            {
                /*
                TRACEF((stderr,"PropertyNotify for window: 0x%x\n",  
                       (unsigned int)event.xproperty.window))
                if( event.xproperty.window == self->root_window )
                    break;

                result = getTree( event.xproperty.window, 
                                      self->display, 
                                      &event,
                                      result );
                */
            }

            case ConfigureNotify:
            {
                break;
            }

            case ClientMessage:
            {
                break;
            }

            case KeyPress:  /* When we impliment the record engine we will
                              need to have this function do more. */
            {
                /*
                TRACEF((stderr,"KeyPress for window: 0x%x\n",  (unsigned int)event.xany.window))
                char buffer_return[30];
                int ret_code = 0;
                KeySym keysym_return;
                ret_code = XLookupString( &event.xkey, 
                                         buffer_return, 
                                         30, 
                                         &keysym_return, 
                                         NULL );

                if (ret_code)
                {
                    buffer_return[ret_code] = '\0';
                    //printf("%x %s, mod: %d\n",  (unsigned int)keysym_return, buffer_return, event.xkey.state);
                }
                */
                break;
            }

            case ReparentNotify:
            {
                TRACEF((stderr,"ReparentNotify for window: 0x%x\n",  (unsigned int)event.xany.window))
                break;
            }

            case KeyRelease:
            {
                break;
            }

            default:
            {
                TRACEF((stderr,"Event Detected: %i (%u)\n", 
                        event.type, (unsigned int)event.xany.window))
                break;
            }
        }/* switch (NextEvent) */
        if( self->event_callback != NULL )
        {
            /* FIXME to be implemented 
            PyObject *ret;
            ret = PyEval_CallObject( self->event_callback, result );
            */
        }
        
        //final_result = PySequence_InPlaceConcat( final_result, result );
        //Py_DECREF( result );    
        
    }/* while */
    if( PyList_Size(result) > 0 )
    {
        TRACEF_NEW_WIN((stderr, "length of window list: %i\n", PyList_Size(result)))
    }
    return (PyListObject *) result;
}

static PyObject *
XDisplay_getRootXWindow( XDisplay *self )
{
    PyObject *result = NULL;
    Window root;
    root = DefaultRootWindow( self->display );
    TRACEF((stderr,"root: 0x%x\n",  (unsigned int)root))
    result = createXWindow( root, self->display, NULL, TRUE );
    return result;
}

static PyListObject *
XWindow_getTree( XWindow *self )
{
    return (PyListObject *) getTree( self->this_window, 
                                         self->this_display, 
                                         NULL,
                                         NULL );
}

static PyObject *
XWindow_isValid( XWindow *self )
{

    if( isValidXWindow( self ) )
    {
        TRACEF((stderr,"Valid window: 0x%x\n",  (unsigned int)self->this_window))
        Py_INCREF(Py_True);
        return Py_True;
    }
    else
    {
        TRACEF((stderr,"Not a valid window: 0x%x\n",  (unsigned int)self->this_window))
        Py_INCREF(Py_False);
        return Py_False;
    }
}

static PyObject *
XWindow_isDestroyed( XWindow *self )
{
    if( self->event_type != XWIN_DESTROYED )
    {
        Py_INCREF(Py_False);
        return Py_False;
    }
    else
    {
        Py_INCREF(Py_True);
        return Py_True;
    }
}
  
static PyObject *
XWindow_isNew( XWindow *self )
{
    if( self->event_type != XWIN_NEW )
    {
        Py_INCREF(Py_False);
        return Py_False;
    }
    else
    {
        Py_INCREF(Py_True);
        return Py_True;
    }
}

static PyObject *
getTree( Window target, Display *display, XEvent *event, PyObject *result_list )
{
    int ret_code, parentRetCode, i;
    Window root_return;
    Window parent_return;
    Window *children_return;
    unsigned int nchildren_return;
 
    PyObject *junk_list = NULL;
    PyObject *tmp_xwindow = NULL;
    parentRetCode = 1;
    if( result_list == NULL )
    {
        /* assume first time we don't have to add target */
        TRACEF((stderr,"Creating new result list\n"))
        result_list =  PyList_New(0);
    }
    
    TRACEF((stderr,"target: 0x%x\n",  (unsigned int)target))
    ret_code = XQueryTree( display, (Window)target, &root_return,
                           &parent_return, &children_return,
                           &nchildren_return );

    if( ret_code != 1 )
    {
        TRACE
        return result_list;
    }
    else
    { 
        tmp_xwindow = createXWindow( target, display, event, FALSE );
        if( tmp_xwindow != NULL )
        {
            PyList_Append( result_list, tmp_xwindow );
        }
    }

    if (nchildren_return == 0)
    {
        TRACEF((stderr,"No children for window 0x%x\n",  (unsigned int)target))
    }
    else
    {
        XSelectInput( display, target, EVENT_MASK );
        for (i = 0; i < nchildren_return; i++)
        {
            TRACEF((stderr,"children_return[%i]: 0x%x\n",  i, (unsigned int)children_return[i]))
            junk_list = getTree( children_return[i], 
                                display, 
                                event, 
                                result_list );
        }
        XFree( children_return );
    }
    return result_list;
}

static PyObject *
XDisplay_getActiveXWindow( XDisplay *self ) 
{
    PyObject *result = NULL;
    Window focus = 0;
    int revert_return;
    XGetInputFocus( self->display, &focus, &revert_return );
    if( focus != None )
    {
        TRACEF((stderr,"focus: 0x%x\n",  (unsigned int)focus))
        result = createXWindow( focus, self->display, NULL, FALSE );
    }
    else
    {
        TRACEF((stderr,"Could not get active window"))
        PyErr_SetString( PyltfxError, "Could not get active window");
    }
    return result;
}

static Window 
getActiveWindow( Display *display )
{
    Window focus;
    Window result = 0;
    int revert_return;
    XGetInputFocus( display, &focus, &revert_return );
    TRACEF((stderr,"focus window: 0x%x\n",  (unsigned int)focus))
    result = getWindow( focus, display );
    TRACEF((stderr,"result window: 0x%x\n",  (unsigned int)result))
    return result;
}

/*
end xdisplay
*/

int 
ErrorHandler(Display *display, XErrorEvent *error)
{
    if ((error->request_code == X_GetWindowAttributes) ||
        (error->request_code == X_ChangeWindowAttributes) ||
        (error->request_code == X_QueryTree) ||
        (error->request_code == X_GetProperty) ||
        (error->request_code == X_ListProperties) ||
        ((error->request_code == X_GetGeometry) &&
        (error->error_code == BadWindow)) ||
        (error->error_code == BadDrawable)) 
    {
        /* skip these error codes */
        return 0;
    }
    else
    {
        char *report = NULL;
        char *err_text = NULL;
        report = malloc(100);
        memset(report, 0, 100);
        err_text = malloc(150);
        memset(err_text, 0, 150);

        XGetErrorText( display, error->error_code, report, 100 );
        TRACEF((stderr,"Xlib Error: <%s>\n", report))
        if( snprintf( err_text, 150, "%s, request code: %i, error code: %i", 
                      report, error->request_code, error->error_code ) >= 150 )
        {
            TRACEF((stderr, "err_text was truncated"))
        }
     
        PyErr_SetString( PyltfxError, err_text);
        free( report ); 
        /* FIXME free( err_text ); */
        return 0;
    }
}


