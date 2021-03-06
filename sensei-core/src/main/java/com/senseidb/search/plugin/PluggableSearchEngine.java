/**
 * This software is licensed to you under the Apache License, Version 2.0 (the
 * "Apache License").
 *
 * LinkedIn's contributions are made under the Apache License. If you contribute
 * to the Software, the contributions will be deemed to have been made under the
 * Apache License, unless you expressly indicate otherwise. Please do not make any
 * contributions that would be inconsistent with the Apache License.
 *
 * You may obtain a copy of the Apache License at http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, this software
 * distributed under the Apache License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the Apache
 * License for the specific language governing permissions and limitations for the
 * software governed under the Apache License.
 *
 * © 2012 LinkedIn Corp. All Rights Reserved.  
 */
package com.senseidb.search.plugin;

import java.util.Comparator;
import java.util.List;
import java.util.Set;

import org.apache.lucene.index.IndexReader;
import org.json.JSONObject;

import com.browseengine.bobo.facets.FacetHandler;
import com.senseidb.conf.SenseiSchema;
import com.senseidb.indexing.ShardingStrategy;
import com.senseidb.plugin.SenseiPluginRegistry;
import com.senseidb.search.node.SenseiCore;

/**
 * While implementing the activity engine John Wang suggested to make its integration with Sensei as generic as possible. This way we can support custom indexers, 
 * store fields w/ index outside of the Lucene and custom facet handlers.
 * By implementing this interface and referencing the implementation class by sensei.search.pluggableEngines.list property inside sensei.properties 
 */
public interface PluggableSearchEngine {
  /**
   * The init callback method, to initialize the custom search engine
   * @param indexDirectory
   * @param nodeId
   * @param senseiSchema
   * @param versionComparator
   * @param pluginRegistry
   * @param shardingStrategy
   */
  public void init(String indexDirectory, int nodeId, SenseiSchema senseiSchema, Comparator<String> versionComparator, SenseiPluginRegistry pluginRegistry, ShardingStrategy shardingStrategy);
  /**
   * @return the biggest version consumed by the engine or null if Sensei should not be aware about the engine's versioning
   */
  public String getVersion();  
  /**
   * Accepts the event new document ot index along with its version. If the event doesn't need to be indexed by the Sensei,return the JsonObject with "type":"skip"
   * @param event
   * @param version
   * @return
   */
  public JSONObject acceptEvent(JSONObject event, String version);
  
  /**
   * @return true if it shouldn't receive the data just for current node's partitions
   */
  public boolean acceptEventsForAllPartitions();
  /**
   * @return field names in the schema, that are managed by this searchEngine, so that they would be ignored core Sensei
   */
  public Set<String> getFieldNames();
  /**
   * @return facet names in the schema, that are managed by this searchEngine, so that they would be ignored core Sensei
   */
  public Set<String> getFacetNames();
  /**
   * @return creates facet handles, that correspond to this customEngine
   */
  public List<FacetHandler<?>> createFacetHandlers();
  /**
   * onDelete callback, that might be used to delete correpsonding data from the custom index
   * @param indexReader
   * @param uids
   */
  public void onDelete(IndexReader indexReader, long... uids);
  /**
   * Is called when the Sensei node has been started
   * @param senseiCore
   */
  public void start(SenseiCore senseiCore);
  /**
   * Sensei Stop callback
   */
  public void stop();  
}
