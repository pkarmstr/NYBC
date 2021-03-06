package org.apache.solr.rest;
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


import org.apache.solr.common.SolrException;
import org.apache.solr.common.SolrException.ErrorCode;
import org.apache.solr.schema.SchemaField;
import org.restlet.representation.Representation;
import org.restlet.resource.ResourceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.UnsupportedEncodingException;

/**
 * This class responds to requests at /solr/(corename)/schema/dynamicfields/pattern
 * where pattern is a field name pattern (with an asterisk at the beginning or the end).
 */
public class DynamicFieldResource extends BaseFieldResource implements GETable {
  private static final Logger log = LoggerFactory.getLogger(DynamicFieldResource.class);

  private static final String DYNAMIC_FIELD = "dynamicfield";

  private String fieldNamePattern;

  public DynamicFieldResource() {
    super();
  }

  /**
   * Gets the field name pattern from the request attribute where it's stored by Restlet. 
   */
  @Override
  public void doInit() throws ResourceException {
    super.doInit();
    if (isExisting()) {
      fieldNamePattern = (String)getRequestAttributes().get(SchemaRestApi.NAME_VARIABLE);
      try {
        fieldNamePattern = null == fieldNamePattern ? "" : urlDecode(fieldNamePattern.trim()).trim();
      } catch (UnsupportedEncodingException e) {
        throw new ResourceException(e);
      }
    }
  }

  @Override
  public Representation get() {
    try {
      if (fieldNamePattern.isEmpty()) {
        final String message = "Dynamic field name is missing";
        throw new SolrException(ErrorCode.BAD_REQUEST, message);
      } else {
        SchemaField field = null;
        for (SchemaField prototype : getSchema().getDynamicFieldPrototypes()) {
          if (prototype.getName().equals(fieldNamePattern)) {
            field = prototype;
            break;
          }
        }
        if (null == field) {
          final String message = "Dynamic field '" + fieldNamePattern + "' not found.";
          throw new SolrException(ErrorCode.NOT_FOUND, message);
        } else {
          getSolrResponse().add(DYNAMIC_FIELD, getFieldProperties(field));
        }
      }
    } catch (Exception e) {
      getSolrResponse().setException(e);
    }
    handlePostExecution(log);

    return new SolrOutputRepresentation();
  }
}
