// -*- lsst-c++ -*-
/*
 * LSST Data Management System
 * Copyright 2008-2013 LSST Corporation.
 *
 * This product includes software developed by the
 * LSST Project (http://www.lsst.org/).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the LSST License Statement and
 * the GNU General Public License along with this program.  If not,
 * see <http://www.lsstcorp.org/LegalNotices/>.
 */

#include "boost/format.hpp"

#include "lsst/pex/exceptions/Exception.h"

/**
 *  Check whether the given values are equal, and throw an LSST Exception with the given message
 *  (which must include two Boost.Format placeholders for the two numbers) if they are not.
 *
 *  For example:
 *  @code
 *  LSST_ASSERT_EQUAL(3, 4, "size of foo (%d) is not equal to size of bar (%d)", LengthErrorException);
 *  @endcode
 */
#define LSST_THROW_IF_NE(N1, N2, EXC_CLASS, MSG)                        \
    if ((N1) != (N2)) throw LSST_EXCEPT(EXC_CLASS, (boost::format(MSG) % (N1) % (N2)).str())
