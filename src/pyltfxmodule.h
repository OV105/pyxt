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

#ifndef _pyltfxmodule_h_
#define _pyltfxmodule_h_ 1

#include <Python.h>

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/keysym.h>
#include <X11/keysymdef.h>
#include <X11/Xproto.h>
#include <X11/Xatom.h>
#include "structmember.h"
#include <unistd.h>
#include <glib.h>

#define MAX_PROPERTY_VALUE_LEN 4096
#define EVENT_MASK SubstructureNotifyMask | PropertyChangeMask | StructureNotifyMask | ExposureMask
#define NO_EVENT -1

#define TRACE_BODY  { \
    fprintf(stderr, "\n*** %s @ %s:%u ***\n", __func__, __FILE__, __LINE__); \
    fflush(stderr); \
}

# define TRACEF_BODY { \
    fprintf(stderr, "\n*** %s @ %s:%u\n",__func__, __FILE__, __LINE__); \
    fprintf a; \
    fflush(stderr); \
}
#ifndef TRUE
# define TRUE 1
#endif

#ifndef FALSE
# define FALSE 0
#endif

#ifdef USE_TRACE_ALL
# define USE_TRACE_KYBD
# define USE_TRACE_EVENTS
# define USE_TRACE_TITLE
# define USE_TRACE_NEW_WIN
#endif

#ifdef USE_TRACE_NEW_WIN
# define TRACE_NEW_WIN TRACE_BODY
# define TRACEF_NEW_WIN(a) { \
    fprintf(stderr, "\n*** %s @ %s:%u\n",__func__, __FILE__, __LINE__); \
    fprintf a; \
    fflush(stderr); \
}
#else
# define TRACE_NEW_WIN
# define TRACEF_NEW_WIN(a) 
#endif

#ifdef USE_TRACE_TITLE
# define TRACE_TITLE TRACE_BODY
# define TRACEF_TITLE(a) { \
    fprintf(stderr, "\n*** %s @ %s:%u\n",__func__, __FILE__, __LINE__); \
    fprintf a; \
    fflush(stderr); \
}
#else
# define TRACE_TITLE
# define TRACEF_TITLE(a) 
#endif

#ifdef USE_TRACE_KYBD
# define TRACE_KYBD TRACE_BODY
# define TRACEF_KYBD(a) { \
    fprintf(stderr, "\n*** %s @ %s:%u\n",__func__, __FILE__, __LINE__); \
    fprintf a; \
    fflush(stderr); \
}
#else
# define TRACE_KYBD
# define TRACEF_KYBD(a) 
#endif

#ifdef USE_TRACE_EVENTS
# define TRACE TRACE_BODY
# define TRACEF(a) { \
    fprintf(stderr, "\n*** %s @ %s:%u\n",__func__, __FILE__, __LINE__); \
    fprintf a; \
    fflush(stderr); \
}
#else
# define TRACE
# define TRACEF(a)
#endif

/* 
    use -DUSE_TRACE_ALL compile option
    examples: 
      TRACEF(("var: %s", var))
      TRACEF(("argv[x=%s] = '%s'\n", x, argv[x]))
*/
#define KEY_ESC 2
#define NUM_MOD_KEYS 3

/*
start module variables
*/

#define XWIN_EMPTY 1
#define XWIN_NEW 2
#define XWIN_DESTROYED 4
#define XWIN_MOUSE_EVENT 8
#define XWIN_KEYPRESS_EVENT 16
#define XWIN_KEYRELEASE_EVENT 32
#define XWIN_OTHER_EVENT 64
#define ALL_EXCEPT_DESTROYED XWIN_NEW|XWIN_MOUSE_EVENT|XWIN_KEYPRESS_EVENT|XWIN_KEYRELEASE_EVENT|XWIN_OTHER_EVENT
#define ALL_EVENTS XWIN_NEW|XWIN_DESTROYED|XWIN_MOUSE_EVENT|XWIN_KEYPRESS_EVENT|XWIN_KEYRELEASE_EVENT|XWIN_OTHER_EVENT

static KeySym; 
keyindex[] = {0, XK_Tab, XK_Shift_L, XK_Control_L, XK_Alt_L, XK_Delete, XK_BackSpace, XK_Return, XK_KP_Enter, XK_F1, XK_F2, XK_F3, XK_F4, XK_F5, XK_F6, XK_F7, XK_F8, XK_F9, XK_F10, XK_F11, XK_F12, XK_Up, XK_Down, XK_Left, XK_Right, XK_Escape, XK_space, XK_Home, XK_End, XK_Page_Up, XK_Page_Down};

static PyObject *key_tab;
static PyObject *key_shift;
static PyObject *key_ctrl;
static PyObject *key_alt;
static PyObject *key_del;
static PyObject *key_bksp;
static PyObject *key_rtrn;
static PyObject *key_enter;
static PyObject *key_f1;
static PyObject *key_f2;
static PyObject *key_f3;
static PyObject *key_f4;
static PyObject *key_f5;
static PyObject *key_f6;
static PyObject *key_f7;
static PyObject *key_f8;
static PyObject *key_f9;
static PyObject *key_f10;
static PyObject *key_f11;
static PyObject *key_f12;
static PyObject *key_up;
static PyObject *key_down;
static PyObject *key_left;
static PyObject *key_right;
static PyObject *key_esc;
static PyObject *key_space;
static PyObject *key_home;
static PyObject *key_end;
static PyObject *key_pgup;
static PyObject *key_pgdown;
/*
end module variables
*/

/*
start module functions
*/
static PyObject *
PyltfxError;

static PyObject *
PyltfxInvalid;

static PyObject *
PyltfxNotFocused;

static PyMethodDef _pyltfx_methods[] = {
    {NULL}  /* Sentinel */
};

static Window
getActiveWindow( Display *display );

static Window
getWindow( Window window, Display *display );

static PyObject *
createXWindow( Window window, 
               Display *display, 
               XEvent *event,
               int no_title );

/*
end module functions
*/

/*
start XWindow
*/

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    int key_state;
    int event_type;
    int no_title;
    int is_window_manager;
    double timestamp;
    Window this_window;
    Window parent_window;
    Display *this_display;
    PyObject *window_title;
    PyObject *key_chars;
    PyObject *window_manager;
} XWindow;

static int
isValidXWindow( XWindow *xwindow );

static void
XWindow_dealloc(XWindow* self);

static PyObject *
XWindow_new( PyTypeObject *type, PyObject *args, PyObject *kwds );

static int
XWindow_init( XWindow *self, PyObject *args, PyObject *kwds );

static int
XWindow_cmp( XWindow *self, XWindow *other );

static long 
XWindow_hash( XWindow *self );

static PyObject * 
XWindow_repr( XWindow *self );

static PyObject * 
XWindow_activate(XWindow* self);

static PyListObject *
XWindow_getTree( XWindow *self );

static PyObject *
XWindow_isValid( XWindow *self );

static PyObject *
XWindow_getTitle( XWindow *self );

static PyObject *
XWindow_isDestroyed( XWindow *self );

static PyObject *
XWindow_isNew( XWindow *self );

static PyObject *
getTree( Window target, Display *display, XEvent *event, PyObject *result_list );

static PyObject * 
XWindow_type(XWindow* self, PyObject *args);

static PyMemberDef XWindow_members[] = {
    {"event_type", T_INT, offsetof(XWindow, event_type), 0,
     "event for xwindow"},
    {"this_window", T_INT, offsetof(XWindow, this_window), 0,
     "xwindow"},
    {"parent_window", T_INT, offsetof(XWindow, parent_window), 0,
     "xwindow"},
    {"this_display", T_INT, offsetof(XWindow, this_display), 0,
     "Window Display"},
    {"is_window_manager", T_INT, offsetof(XWindow, is_window_manager), 0,
     "True if window manager"},
    {"timestamp", T_DOUBLE, offsetof(XWindow, timestamp), 0,
     "Event timestamp"},
    {"window_title", T_OBJECT_EX, offsetof(XWindow, window_title), 0,
     "Window Title"},
    {"key_chars", T_OBJECT_EX, offsetof(XWindow, key_chars), 0,
     "key event characters"},
    {"window_manager", T_OBJECT_EX, offsetof(XWindow, window_manager), 0,
     "Window manager"},
    {NULL}  /* Sentinel */
};

static PyMethodDef XWindow_methods[] = {
    {"type", (PyCFunction)XWindow_type, METH_VARARGS,
     "Type character"
    },
    {"activate", (PyCFunction)XWindow_activate, METH_NOARGS,
     "Make window active"
    },
    {"isValid", (PyCFunction)XWindow_isValid, METH_NOARGS,
     "Window is valid"
    },
    {"getTitle", (PyCFunction)XWindow_getTitle, METH_NOARGS,
     "Get title of window"
    },
    {"isDestroyed", (PyCFunction)XWindow_isDestroyed, METH_NOARGS,
     "Window is not valid"
    },
    {"isNew", (PyCFunction)XWindow_isNew, METH_NOARGS,
     "Window is new"
    },
    {"getTree", (PyCFunction)XWindow_getTree, METH_NOARGS,
     "Return list of window and children"
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject XWindowType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "pyltfx.XWindow",             /*tp_name*/
    sizeof(XWindow),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)XWindow_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    (cmpfunc)XWindow_cmp,      /*tp_compare*/
    (reprfunc)XWindow_repr,    /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    (hashfunc)XWindow_hash,    /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "XWindow objects",           /* tp_doc */
            0,               /* tp_traverse */
            0,               /* tp_clear */
            0,               /* tp_richcompare */
            0,               /* tp_weaklistoffset */
            0,               /* tp_iter */
            0,               /* tp_iternext */
    XWindow_methods,             /* tp_methods */
    XWindow_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)XWindow_init,      /* tp_init */
    0,                         /* tp_alloc */
    XWindow_new,                 /* tp_new */
};
#define is_xwindow(x) ((x)->ob_type == &XWindowType)
/*
end XWindow
*/


/*
start XDisplay
*/

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    char *display_string;
    Display *display;
    Window root_window;
    PyObject *root_xwindow;
    char *xdisplay_char;
    PyObject *xdisplay_string;
    PyObject *event_callback;
} XDisplay;

static void
XDisplay_dealloc(XDisplay* self);

static int
XDisplay_init(XDisplay *self, PyObject *args, PyObject *kwds);

static PyObject *
XDisplay_getActiveXWindow( XDisplay *self);

static PyObject *
XDisplay_getRootXWindow( XDisplay *self );

static PyObject *
XDisplay_setXEventCallback( XDisplay *self, PyObject *args );

static PyListObject *
XDisplay_checkXEvent( XDisplay *self );

int ErrorHandler( Display*, XErrorEvent* );

static PyMemberDef XDisplay_members[] = {
    {"xdisplay_string", T_OBJECT_EX, offsetof(XDisplay, xdisplay_string), 0,
     "xwindow display string"},
    {"event_callback", T_OBJECT_EX, offsetof(XDisplay, event_callback), 0,
     "X event call back function"},
    {"root_xwindow", T_OBJECT_EX, offsetof(XDisplay, root_xwindow), 0,
     "Root XWindow"},
    {NULL}  /* Sentinel */
};

static PyMethodDef XDisplay_methods[] = {
    {"setXEventCallback", (PyCFunction)XDisplay_setXEventCallback, METH_VARARGS,
     "Set call back for X event"
    },
    {"getRootXWindow", (PyCFunction)XDisplay_getRootXWindow, METH_NOARGS,
     "Return root window"
    },
    {"getActiveXWindow", (PyCFunction)XDisplay_getActiveXWindow, METH_NOARGS,
     "Return the title of the window"
    },
    {"checkXEvent", (PyCFunction)XDisplay_checkXEvent, METH_NOARGS,
     "check for X events"
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject XDisplayType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "pyltfx.XDisplay",             /*tp_name*/
    sizeof(XDisplay),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)XDisplay_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "XDisplay objects",           /* tp_doc */
            0,               /* tp_traverse */
            0,               /* tp_clear */
            0,               /* tp_richcompare */
            0,               /* tp_weaklistoffset */
            0,               /* tp_iter */
            0,               /* tp_iternext */
    XDisplay_methods,             /* tp_methods */
    XDisplay_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)XDisplay_init,      /* tp_init */
    0,                         /* tp_alloc */
    PyType_GenericNew,           /* tp_new */
};
#define is_xdisplay(x) ((x)->ob_type == &XDisplayType)
/*
end XDisplay
*/

#ifndef PyMODINIT_FUNC/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif


#endif /* _pyltfxmodule_h_ */
