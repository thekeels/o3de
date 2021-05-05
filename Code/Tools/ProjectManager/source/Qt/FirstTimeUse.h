/*
 * All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
 * its licensors.
 *
 * For complete copyright and license terms please see the LICENSE at the root of this
 * distribution (the "License"). All use of this software is governed by the License,
 * or, if provided, by the license below or the license accompanying this file. Do not
 * remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *
 */
#pragma once

#if !defined(Q_MOC_RUN)
#include <Qt/ScreenWidget.h>
#endif

namespace Ui
{
    class FirstTimeUseClass;
}

namespace O3DE::ProjectManager
{
    class FirstTimeUse
        : public ScreenWidget
    {
    public:
        explicit FirstTimeUse(ProjectManagerWindow* window);
        ~FirstTimeUse();

    protected:
        void ConnectSlotsAndSignals() override;

    protected slots:
        void HandleNewProjectButton();
        void HandleOpenProjectButton();

    private:
        QScopedPointer<Ui::FirstTimeUseClass> m_ui;
    };

} // namespace O3DE::ProjectManager