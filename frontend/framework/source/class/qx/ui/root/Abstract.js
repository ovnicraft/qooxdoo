/* ************************************************************************

   qooxdoo - the new era of web development

   http://qooxdoo.org

   Copyright:
     2004-2008 1&1 Internet AG, Germany, http://www.1und1.de

   License:
     LGPL: http://www.gnu.org/licenses/lgpl.html
     EPL: http://www.eclipse.org/org/documents/epl-v10.php
     See the LICENSE file in the project's top-level directory for details.

   Authors:
     * Sebastian Werner (wpbasti)
     * Fabian Jakobs (fjakobs)

************************************************************************ */

/**
 * Shared implementation for all root widgets.
 */
qx.Class.define("qx.ui.root.Abstract",
{
  extend : qx.ui.core.Widget,
  include : [ qx.ui.core.MChildren, qx.ui.core.MLayoutHandling ],



  /*
  *****************************************************************************
     CONSTRUCTOR
  *****************************************************************************
  */

  construct : function()
  {
    this.base(arguments);

    this._focusHandler = new qx.ui.core.FocusHandler(this);
  },




  /*
  *****************************************************************************
     PROPERTIES
  *****************************************************************************
  */

  properties :
  {
    // overridden
    appearance :
    {
      refine : true,
      init : "root"
    },

    // overridden
    enabled :
    {
      refine : true,
      init : true
    },

    // overridden
    focusable :
    {
      refine : true,
      init : true
    }
  },




  /*
  *****************************************************************************
     MEMBERS
  *****************************************************************************
  */

  members :
  {
    // overridden
    isRootWidget : function() {
      return true;
    },


    // overridden
    isLayoutRoot : function() {
      return true;
    },


    // overridden
    isFocusRoot : function() {
      return true;
    }
  },




  /*
  *****************************************************************************
     DEFER
  *****************************************************************************
  */

  defer : function(statics, members)
  {
    qx.ui.core.MChildrenHandling.remap(members);
    qx.ui.core.MLayoutHandling.remap(members);
  },



  /*
  *****************************************************************************
     DESTRUCTOR
  *****************************************************************************
  */

  destruct : function() {
    this._disposeObjects("_focusHandler");
  }
});
